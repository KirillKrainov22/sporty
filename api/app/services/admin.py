from typing import List

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.models.activity import Activity


async def get_all_users(db: AsyncSession) -> List[User]:
    stmt = select(User).order_by(User.id)
    result = await db.execute(stmt)
    return result.scalars().all()


async def set_ban_status(db: AsyncSession, user_id: int, is_banned: bool) -> User | None:
    # можно через db.get, но чтобы быть ближе к твоему стилю — через select
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if user is None:
        return None

    user.is_banned = is_banned
    await db.commit()
    await db.refresh(user)
    return user


async def add_points(db: AsyncSession, user_id: int, amount: int) -> User | None:
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if user is None:
        return None

    user.points += amount
    await db.commit()
    await db.refresh(user)
    return user


async def get_system_statistics(db: AsyncSession) -> dict:
    # Общее количество пользователей
    total_users = (
        await db.execute(select(func.count(User.id)))
    ).scalar_one()

    # Активные пользователи за сегодня (по активностям)
    active_today = (
        await db.execute(
            select(func.count(func.distinct(Activity.user_id)))
            .where(func.date(Activity.created_at) == func.current_date())
        )
    ).scalar_one() or 0

    # Общее количество активностей
    total_activities = (
        await db.execute(select(func.count(Activity.id)))
    ).scalar_one()

    # Активности по типам
    rows = await db.execute(
        select(Activity.type, func.count(Activity.id))
        .group_by(Activity.type)
    )
    activities_by_type = {row[0]: row[1] for row in rows.all()}

    # Суммарные очки
    total_points = (
        await db.execute(select(func.coalesce(func.sum(User.points), 0)))
    ).scalar_one()

    # Топ 5 пользователей по очкам
    top_users_result = await db.execute(
        select(User).order_by(User.points.desc()).limit(5)
    )
    top_users = top_users_result.scalars().all()

    return {
        "total_users": int(total_users),
        "active_users_today": int(active_today),
        "total_activities": int(total_activities),
        "activities_by_type": activities_by_type,
        "total_points": int(total_points),
        "top_users": top_users,
    }