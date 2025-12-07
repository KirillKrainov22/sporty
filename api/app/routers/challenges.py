from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db import get_session
from app.models.challenge import Challenge
from app.models.user import User
from app.schemas.challenge import ChallengeCreate, ChallengeRead

router = APIRouter(prefix="/api/challenges", tags=["Challenges"])


@router.post("/", response_model=ChallengeRead)
async def create_challenge(payload: ChallengeCreate, db: AsyncSession = Depends(get_session)):
    # Проверяем: существуют ли оба пользователя
    for user_id in [payload.creator_id, payload.target_id]:
        result = await db.execute(select(User).where(User.id == user_id))
        if not result.scalar_one_or_none():
            raise HTTPException(status_code=404, detail=f"User {user_id} not found")

    # Создаём челлендж
    challenge = Challenge(
        creator_id=payload.creator_id,
        target_id=payload.target_id,
        type=payload.type,
    )

    db.add(challenge)
    await db.commit()
    await db.refresh(challenge)

    return challenge


@router.get("/{challenge_id}", response_model=ChallengeRead)
async def get_challenge(challenge_id: int, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Challenge).where(Challenge.id == challenge_id))
    challenge = result.scalar_one_or_none()

    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")

    return challenge
