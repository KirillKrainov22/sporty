from datetime import datetime, time

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Activity


BASE_POINTS = {
    "run": 10,      # points per km
    "bicycle": 5,
    "swim": 15,
    "workout": 8,  # per 30 min, treated as distance multiplier
}


def parse_datetime(dt_value: datetime) -> datetime:
    if isinstance(dt_value, datetime):
        return dt_value

    try:
        return datetime.fromisoformat(str(dt_value).replace("Z", "+00:00"))
    except Exception:
        return datetime.utcnow()


def is_morning(created_at: datetime) -> bool:
    return time(5, 0) <= created_at.time() < time(12, 0)


def is_weekend(created_at: datetime) -> bool:
    return created_at.weekday() >= 5


async def is_personal_best(
    session: AsyncSession, user_id: int, distance: float | None, activity_id: int | None
) -> bool:
    if distance is None:
        return False

    result = await session.execute(
        select(func.max(Activity.distance)).where(
            Activity.user_id == user_id,
            Activity.id != activity_id,
        )
    )
    best_distance = result.scalar()
    if best_distance is None:
        return True

    try:
        return float(distance) > float(best_distance)
    except Exception:
        return False


async def calculate_points(session: AsyncSession, activity: Activity) -> int:
    base = BASE_POINTS.get(activity.type)
    if base is None:
        return 0

    created_at = parse_datetime(activity.created_at)
    distance = activity.distance or 0

    points = base * distance
    if is_morning(created_at):
        points *= 2
    if is_weekend(created_at):
        points *= 1.5

    if await is_personal_best(session, activity.user_id, activity.distance, activity.id):
        points += 50

    return int(points)


def calculate_level(total_points: int, current_level: int | None = None) -> int:
    # Simple leveling algorithm: every 1000 points -> +1 level
    base_level = current_level or 1
    computed_level = max(1, total_points // 1000 + 1)
    return max(base_level, computed_level)