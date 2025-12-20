import asyncio
import json
import logging
from aiokafka import AIOKafkaConsumer
from aiokafka.errors import KafkaConnectionError


# -------------------- logging --------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger("worker")


# -------------------- utils --------------------
def safe_json_loads(raw: bytes | None):
    
    if raw is None:
        return None

    try:
        text = raw.decode().strip()
        if not text:
            return None
        return json.loads(text)
    except Exception:
        return None


# -------------------- main logic --------------------
async def main():
    consumer = AIOKafkaConsumer(
        "activities_created",
        bootstrap_servers="kafka:9092",
        group_id="sporty-workers",
        auto_offset_reset="earliest",
        enable_auto_commit=True,
    )

    # ---- wait for Kafka ----
    while True:
        try:
            await consumer.start()
            logger.info("WORKER CONNECTED TO KAFKA")
            break
        except KafkaConnectionError:
            logger.warning("KAFKA NOT READY, RETRY IN 5 SECONDS...")
            await asyncio.sleep(5)

    try:
        async for msg in consumer:
            payload = safe_json_loads(msg.value)

            if payload is None:
                logger.warning("SKIPPED EMPTY OR INVALID MESSAGE")
                continue

            # business logic
            logger.info(f"RECEIVED MESSAGE: {payload}")


    except Exception as e:
        logger.exception(f"WORKER CRUSHED: {e}")

    finally:
        await consumer.stop()
        logger.info("WORKER STOPPED")


# -------------------- entrypoint --------------------
if __name__ == "__main__":
    asyncio.run(main())
