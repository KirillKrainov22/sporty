# worker/consumers/activities.py
import json

from aiokafka import AIOKafkaConsumer


from db.session import AsyncSessionLocal
from utils.idempotency import check_and_mark
from services.stats_service import recalc_user_stats
from services.achievement_service import check_achievements
from repositories.activity_repo import get_total_points


async def consume_activities():
    consumer = AIOKafkaConsumer(
        "activities_created",
        bootstrap_servers="kafka:9092",
        group_id="activities_group",
    )

    await consumer.start()
    try:
        async for msg in consumer:
            data = json.loads(msg.value)
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