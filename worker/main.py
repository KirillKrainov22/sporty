import asyncio
from worker.consumers.activities import consume_activities

if __name__ == "__main__":
    asyncio.run(consume_activities())