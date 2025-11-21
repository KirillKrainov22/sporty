from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select

from app.db import get_db
from app.models.activity import Activity
from app.models.user import User
from app.schemas.activity import ActivityCreate, ActivityRead

router = APIRouter(tags=["Activities"])


@router.post(
    "/activities",
    response_model=ActivityRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_activity(
    activity_in: ActivityCreate,
    db: AsyncSession = Depends(get_db),
):
    # Проверяем, что юзер существует
    result = await db.execute(select(User).where(User.id == activity_in.user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    activity = Activity(
        user_id=activity_in.user_id,
        type=activity_in.type,
        distance=activity_in.distance,
        duration=activity_in.duration,
    )

    db.add(activity)
    # Очки, уровень и т.п. можно посчитать в воркере, но для демо можно начислить тут
    await db.commit()
    await db.refresh(activity)
    return activity
