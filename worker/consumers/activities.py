# worker/consumers/activities.py
import asyncio
import json
import logging

from aiokafka import AIOKafkaConsumer
from aiokafka.errors import (
    GroupCoordinatorNotAvailableError,
    KafkaConnectionError,
    KafkaError,
    UnknownTopicOrPartitionError,
)

from worker.db.session import AsyncSessionLocal
from worker.repositories.activity_repo import get_total_points
from worker.services.achievement_service import check_achievements
from worker.services.stats_service import recalc_user_stats
from worker.utils.idempotency import check_and_mark

logger = logging.getLogger(__name__)


async def _start_consumer_with_retry(consumer: AIOKafkaConsumer, topic: str):
    while True:
        try:
            await consumer.start()
            partitions = await consumer.partitions_for_topic(topic)

            # Topic metadata might not be available immediately after creation
            if partitions is None or len(partitions) == 0:
                raise UnknownTopicOrPartitionError(f"Topic {topic} is not ready yet")

            logger.info("Connected to Kafka and found topic %s", topic)
            return
        except (
            GroupCoordinatorNotAvailableError,
            UnknownTopicOrPartitionError,
            KafkaConnectionError,
            KafkaError,
        ) as exc:
            logger.warning(
                "Kafka not ready for topic %s (%s). Retrying in 2 seconds...",
                topic,
                exc,
            )
            try:
                await consumer.stop()
            except Exception:
                # If stopping fails, just continue to retry
                pass
            await asyncio.sleep(2)


async def consume_activities():
    consumer = AIOKafkaConsumer(
        "activities_created",
        bootstrap_servers="kafka:9092",
        group_id="activities_group",
    )

    await _start_consumer_with_retry(consumer, "activities_created")
    try:
        async for msg in consumer:
            try:
                data = json.loads(msg.value)
            except json.JSONDecodeError:
                logger.warning("Received malformed JSON message: %s", msg.value)
                continue

            required_fields = ["event_id", "activity_id", "user_id"]
            missing = [field for field in required_fields if field not in data]
            if missing:
                logger.warning(
                    "Skipping message missing fields %s: %s", ", ".join(missing), data
                )
                continue

            event_id = data["event_id"]
            user_id = data["user_id"]

            async with AsyncSessionLocal() as session:
                already = await check_and_mark(session, event_id)
                if already:
                    continue

                await recalc_user_stats(session, user_id)
                total = await get_total_points(session, user_id)
                await check_achievements(session, user_id, total)

                await session.commit()
    finally:
        await consumer.stop()