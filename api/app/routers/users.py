from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.models.user import User
from app.schemas.user import UserCreate, UserRead
from app.models.activity import Activity
from app.schemas.user import UserStats


router = APIRouter(prefix="/api/users", tags=["Users"])

# ------------------------------
# 1) CREATE USER
# ------------------------------
@router.post("/", response_model=UserRead)
async def create_user(data: UserCreate, session: AsyncSession = Depends(get_session)):
    # Проверяем, есть ли пользователь
    result = await session.execute(select(User).where(User.telegram_id == data.telegram_id))
    existing_user = result.scalar_one_or_none()

    if existing_user:
        return existing_user

    new_user = User(
        telegram_id=data.telegram_id,
        username=data.username,
        points=0,
        level=1
    )

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return new_user


# ------------------------------
# 2) GET USER BY TELEGRAM ID
# ------------------------------
@router.get("/{telegram_id}", response_model=UserRead)
async def get_user(telegram_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User).where(User.telegram_id == telegram_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

@router.get("/{user_id}/stats", response_model=UserStats)
async def get_user_stats(
    user_id: int,
    db: AsyncSession = Depends(get_session),
):
    # 1. Получаем пользователя
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # 2. Суммарные данные по активностям
    summary_stmt = (
        select(
            func.count(Activity.id),
            func.coalesce(func.sum(Activity.distance), 0.0),
            func.coalesce(func.sum(Activity.duration), 0),
        )
        .where(Activity.user_id == user_id)
    )
    total_activities, total_distance, total_duration = (
        await db.execute(summary_stmt)
    ).one()

    # 3. Прогресс по дням
    daily_stmt = (
        select(
            func.date_trunc("day", Activity.created_at).label("day"),
            func.coalesce(func.sum(Activity.points), 0).label("points")
        )
        .where(Activity.user_id == user_id)
        .group_by("day")
        .order_by("day")
    )
    daily_rows = (await db.execute(daily_stmt)).all()
    daily_progress = [
        {"date": row.day.date(), "points": int(row.points)}
        for row in daily_rows
    ]

    # 4. Прогресс по неделям
    weekly_stmt = (
        select(
            func.date_trunc("week", Activity.created_at).label("week_start"),
            func.coalesce(func.sum(Activity.points), 0).label("points")
        )
        .where(Activity.user_id == user_id)
        .group_by("week_start")
        .order_by("week_start")
    )
    weekly_rows = (await db.execute(weekly_stmt)).all()
    weekly_progress = [
        {"week_start": row.week_start.date(), "points": int(row.points)}
        for row in weekly_rows
    ]

    # 5. Статистика по типам активностей
    type_stmt = (
        select(
            Activity.type.label("type"),
            func.count(Activity.id).label("count"),
            func.coalesce(func.sum(Activity.distance), 0.0).label("distance"),
            func.coalesce(func.sum(Activity.duration), 0).label("duration"),
        )
        .where(Activity.user_id == user_id)
        .group_by(Activity.type)
    )
    type_rows = (await db.execute(type_stmt)).all()
    activity_type_stats = [
        {
            "type": row.type,
            "count": int(row.count),
            "distance": float(row.distance),
            "duration": int(row.duration),
        }
        for row in type_rows
    ]

    # 6. Место в глобальном рейтинге
    rank_stmt = select(func.count(User.id)).where(
        User.points > user.points,
        User.is_banned == False
    )
    higher_count = (await db.execute(rank_stmt)).scalar_one()
    global_rank = higher_count + 1

    return UserStats(
        user_id=user.id,
        username=user.username,
        points=user.points,
        level=user.level,

        total_activities=int(total_activities),
        total_distance=float(total_distance),
        total_duration=int(total_duration),

        global_rank=global_rank,
        daily_progress=daily_progress,
        weekly_progress=weekly_progress,
        activity_type_stats=activity_type_stats,
    )
