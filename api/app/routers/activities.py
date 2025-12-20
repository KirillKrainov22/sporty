from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db import get_session
from app.models.activity import Activity
from app.schemas.activity import ActivityCreate, ActivityRead
#from app.core.kafka_producer import send_kafka_message
from app.models.user import User

router = APIRouter(
    prefix="/api/activities",
    tags=["Activities"]
)

@router.post("/", response_model=ActivityRead)
async def create_activity(
    data: ActivityCreate,
    db: AsyncSession = Depends(get_session)
):
    
    user = await db.get(User, data.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.is_banned:
        raise HTTPException(status_code=403, detail="User is banned")

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
    # await send_kafka_message("activities_created", {
    #     "activity_id": activity.id,
    #     "user_id": activity.user_id,
    #     "type": activity.type,
    #     "distance": activity.distance,
    #     "duration": activity.duration,
    #     "created_at": activity.created_at.isoformat()
    # })
    return activity
