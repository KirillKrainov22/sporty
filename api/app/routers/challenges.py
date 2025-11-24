from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.models.challenge import Challenge
from app.models.user import User
from app.schemas.challenge import ChallengeCreate, ChallengeRead

router = APIRouter(tags=["Challenges"])


@router.post(
    "/challenges",
    response_model=ChallengeRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_challenge(
    challenge_in: ChallengeCreate,
    db: AsyncSession = Depends(get_db),
):
    # Проверяем, что оба участника существуют
    result = await db.execute(select(User).where(User.id == challenge_in.creator_id))
    creator = result.scalar_one_or_none()
    result = await db.execute(select(User).where(User.id == challenge_in.target_id))
    target = result.scalar_one_or_none()

    if not creator or not target:
        raise HTTPException(status_code=404, detail="Creator or target not found")

    challenge = Challenge(
        creator_id=challenge_in.creator_id,
        target_id=challenge_in.target_id,
        type=challenge_in.type,
        start_date=challenge_in.start_date,
        end_date=challenge_in.end_date,
    )
    db.add(challenge)
    await db.commit()
    await db.refresh(challenge)
    return challenge


@router.get("/challenges/{challenge_id}", response_model=ChallengeRead)
async def get_challenge(
    challenge_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Challenge).where(Challenge.id == challenge_id))
    challenge = result.scalar_one_or_none()
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")
    return challenge
