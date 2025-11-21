from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.models.user import User
from app.models.activity import Activity
from app.schemas.user import UserRead, UserStats, UserCreate
from app.schemas.friend import FriendRead
from app.models.friend import Friend

router = APIRouter(tags=["Users"])


@router.post("/users", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    # Проверим, что такого telegram_id ещё нет
    result = await db.execute(
        select(User).where(User.telegram_id == user_in.telegram_id)
    )
    existing = result.scalar_one_or_none()
    if existing:
        return existing

    user = User(
        telegram_id=user_in.telegram_id,
        username=user_in.username,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@router.get("/users/{user_id}", response_model=UserRead)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/users/{user_id}/stats", response_model=UserStats)
async def get_user_stats(
    user_id: int,
    db: AsyncSession = Depends(get_db),
):
    # Проверим, что юзер существует
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Считаем агрегаты по Activity
    result = await db.execute(
        select(
            func.count(Activity.id),
            func.coalesce(func.sum(Activity.distance), 0.0),
            func.coalesce(func.sum(Activity.duration), 0),
        ).where(Activity.user_id == user_id)
    )
    total_activities, total_distance, total_duration = result.one()

    return UserStats(
        user_id=user_id,
        total_points=user.points,
        total_activities=total_activities,
        total_distance=float(total_distance),
        total_duration=int(total_duration),
    )


@router.get(
    "/users/{user_id}/friends",
    response_model=List[FriendRead],
)
async def get_user_friends(
    user_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Friend).where(Friend.user_id == user_id)
    )
    friends = result.scalars().all()
    return friends
