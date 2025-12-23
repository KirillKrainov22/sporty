from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.kafka_producer import send_kafka_message
from app.db import get_session
from app.models import Activity, User
from app.schemas.activity import ActivityCreate, ActivityRead
from app.services.points import calculate_level, calculate_points

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
    )
    db.add(activity)
    await db.flush()
    await db.refresh(activity)

    points = await calculate_points(db, activity)
    activity.points = points

    user.points = (user.points or 0) + points
    user.level = calculate_level(user.points, user.level)
    await db.flush()
    await db.commit()
    await db.refresh(activity)
    await send_kafka_message("activities_created", {
        "activity_id": activity.id,
        "user_id": activity.user_id,
        "type": activity.type,
        "distance": activity.distance,
        "duration": activity.duration,
        "created_at": activity.created_at.isoformat(),
        "points": activity.points,
    })
    return activity
