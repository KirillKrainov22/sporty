from aiokafka import AIOKafkaProducer
from app.core.config import settings
producer: AIOKafkaProducer | None = None

async def init_kafka_producer():
    global producer

    print(f"Connecting to Kafka at: {settings.kafka_bootstrap_servers}")

    producer = AIOKafkaProducer(
        bootstrap_servers=settings.kafka_bootstrap_servers
    )
    await producer.start()
    print("Kafka Producer started")

async def send_kafka_message(topic: str, message: dict):
    if producer is None:
        raise RuntimeError("Kafka producer is not initialized")

    import json
    await producer.send_and_wait(topic, json.dumps(message).encode("utf-8"))

async def close_kafka_producer():
    global producer
    if producer is not None:
        await producer.stop()
        print("Kafka Producer stopped")
