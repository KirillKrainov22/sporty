from sqlalchemy import text


async def is_processed(session, event_id: str) -> bool:
    res = await session.execute(
        text("SELECT 1 FROM processed_events WHERE event_id = :eid"),
        {"eid": event_id},
    )
    return res.first() is not None


async def mark_processed(session, event_id: str):
    await session.execute(
        text(
            """
            INSERT INTO processed_events(event_id)
            VALUES (:eid)
            ON CONFLICT DO NOTHING
            """
        ),
        {"eid": event_id},
    )