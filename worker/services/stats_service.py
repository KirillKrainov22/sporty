# worker/services/stats_service.py
from worker.repositories.activity_repo import (
    get_total_points,
    get_daily_points,
)
from worker.repositories.stats_repo import upsert_user_stats
from worker.services.level_service import calc_level

async def recalc_user_stats(session, user_id: int):
    total = await get_total_points(session, user_id)
    daily = await get_daily_points(session, user_id)

    if daily:
        max_day = max(d["points"] for d in daily)
        avg = total / len(daily)
    else:
        max_day = 0
        avg = 0.0

    level = calc_level(total)

    await upsert_user_stats(
        session=session,
        user_id=user_id,
        total=total,
        avg=avg,
        max_day=max_day,
        level=level,
    )