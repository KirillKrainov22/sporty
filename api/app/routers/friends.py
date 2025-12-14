from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db import get_session
from app.models.friend import Friend
from app.models.user import User
from app.schemas.friend import FriendCreate, FriendRead

router = APIRouter(prefix="/api/friends", tags=["Friends"])


@router.post("/", response_model=FriendRead)
async def add_friend(payload: FriendCreate, db: AsyncSession = Depends(get_session)):
    # Проверяем, что оба юзера существуют
    result_user = await db.execute(select(User).filter(User.id == payload.user_id))
    user = result_user.scalars().first()

    result_friend = await db.execute(select(User).filter(User.id == payload.friend_id))
    friend = result_friend.scalars().first()

    if not user or not friend:
        raise HTTPException(status_code=404, detail="User not found")

    if user.is_banned:
        raise HTTPException(status_code=403, detail="User is banned")

    if friend.is_banned:
        raise HTTPException(status_code=403, detail="Target user is banned")
    if payload.user_id == payload.friend_id:
        raise HTTPException(status_code=400, detail="Cannot add yourself as friend")

    # Создаём запись дружбы
    new_friend = Friend(
        user_id=payload.user_id,
        friend_id=payload.friend_id,
        status="pending"
    )

    db.add(new_friend)
    await db.commit()
    await db.refresh(new_friend)

    return new_friend


@router.get("/users/{user_id}", response_model=list[FriendRead])
async def get_friends(user_id: int, db: AsyncSession = Depends(get_session)):
    result = await db.execute(
        select(Friend).filter(Friend.user_id == user_id)
    )
    friends = result.scalars().all()
    return friends
