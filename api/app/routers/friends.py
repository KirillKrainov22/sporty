from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.models.friend import Friend
from app.models.user import User
from app.schemas.friend import FriendCreate, FriendRead

router = APIRouter(tags=["Friends"])


@router.post(
    "/friends",
    response_model=FriendRead,
    status_code=status.HTTP_201_CREATED,
)
async def add_friend(
    friend_in: FriendCreate,
    db: AsyncSession = Depends(get_db),
):
    # Проверим, что оба пользователя существуют
    result = await db.execute(select(User).where(User.id == friend_in.user_id))
    user = result.scalar_one_or_none()
    result = await db.execute(select(User).where(User.id == friend_in.friend_id))
    friend_user = result.scalar_one_or_none()

    if not user or not friend_user:
        raise HTTPException(status_code=404, detail="User or friend not found")

    relation = Friend(
        user_id=friend_in.user_id,
        friend_id=friend_in.friend_id,
        status=friend_in.status,
    )
    db.add(relation)
    await db.commit()
    await db.refresh(relation)
    return relation
