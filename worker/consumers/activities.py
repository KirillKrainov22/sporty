# worker/consumers/activities.py
import json
from aiokafka import AIOKafkaConsumer

async def consume_activities():
    consumer = AIOKafkaConsumer(
        "activities_created",
        bootstrap_servers="kafka:9092",
        group_id="activities_group"
    )

    await consumer.start()
    try:
        async for msg in consumer:
            activity = json.loads(msg.value)
            print("Received activity:", activity)
    finally:
        await consumer.stop()