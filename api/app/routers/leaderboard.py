from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.models.user import User
from app.models.friend import Friend
from app.schemas.user import UserRead

router = APIRouter(tags=["Leaderboard"])


@router.get("/leaderboard", response_model=List[UserRead])
async def get_global_leaderboard(
    limit: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(User).order_by(User.points.desc()).limit(limit)
    )
    users = result.scalars().all()
    return users


@router.get("/leaderboard/friends", response_model=List[UserRead])
async def get_friends_leaderboard(
    user_id: int,
    db: AsyncSession = Depends(get_db),
):
    # Проверяем, что юзер есть
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Подзапрос с id друзей
    friends_subq = (
        select(Friend.friend_id)
        .where(Friend.user_id == user_id)
        .subquery()
    )

    result = await db.execute(
        select(User)
        .where(User.id.in_(friends_subq))
        .order_by(User.points.desc())
    )
    friends = result.scalars().all()
    return friends
