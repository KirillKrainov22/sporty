# worker/repositories/activity_repo.py
from sqlalchemy import text


async def get_total_points(session, user_id: int) -> int:
    res = await session.execute(
        text(
            """
            SELECT COALESCE(SUM(points), 0)
            FROM activities
            WHERE user_id = :uid
            """
        ),
        {"uid": user_id},
    )
    return res.scalar_one()


async def get_daily_points(session, user_id: int):
    res = await session.execute(
        text(
            """
            SELECT DATE(created_at) as day, SUM(points) as points
            FROM activities
            WHERE user_id = :uid
            GROUP BY DATE(created_at)
            """
        ),
        {"uid": user_id},
    )
    return res.mappings().all()