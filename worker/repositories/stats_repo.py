# worker/repositories/stats_repo.py
from sqlalchemy import text

async def upsert_user_stats(
    session,
    user_id: int,
    total: int,
    avg: float,
    max_day: int,
    level: int,
):
    await session.execute(
        text("""
            INSERT INTO user_stats(user_id, total_points, avg_points_per_day, max_points_per_day, level)
            VALUES (:uid, :t, :a, :m, :lvl)
            ON CONFLICT (user_id) DO UPDATE SET
                total_points = EXCLUDED.total_points,
                avg_points_per_day = EXCLUDED.avg_points_per_day,
                max_points_per_day = EXCLUDED.max_points_per_day,
                level = EXCLUDED.level
        """),
        {
            "uid": user_id,
            "t": total,
            "a": avg,
            "m": max_day,
            "lvl": level,
        },
    )