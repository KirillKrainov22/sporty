from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db import get_session
from app.models.activity import Activity
from app.schemas.activity import ActivityCreate, ActivityRead

router = APIRouter(
    prefix="/api/activities",
    tags=["Activities"]
)

@router.post("/", response_model=ActivityRead)
async def create_activity(
    data: ActivityCreate,
    db: AsyncSession = Depends(get_session)
):
    activity = Activity(
        user_id=data.user_id,
        type=data.type,
        distance=data.distance,
        duration=data.duration,
        points=0  # временно, пока нет воркера
    )
    db.add(activity)
    await db.commit()
    await db.refresh(activity)
    return activity
