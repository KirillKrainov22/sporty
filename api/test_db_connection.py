import asyncio
from sqlalchemy import text
from common.db import engine

async def test():
    try:
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            print("DB connection OK:", result.scalar())
    except Exception as e:
        print("DB connection FAILED:", e)

asyncio.run(test())