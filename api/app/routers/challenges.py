from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db import get_session
from app.models import Challenge
from app.models import User
from app.schemas.challenge import ChallengeCreate, ChallengeRead

router = APIRouter(prefix="/api/challenges", tags=["Challenges"])


@router.post("/", response_model=ChallengeRead)
async def create_challenge(payload: ChallengeCreate, db: AsyncSession = Depends(get_session)):
    # Проверяем: существуют ли оба пользователя
    # Проверяем creator
    result = await db.execute(select(User).where(User.id == payload.creator_id))
    creator = result.scalar_one_or_none()

    if not creator:
        raise HTTPException(status_code=404, detail="Creator not found")

    if creator.is_banned:
        raise HTTPException(status_code=403, detail="Creator is banned")

    # Проверяем target
    result = await db.execute(select(User).where(User.id == payload.target_id))
    target = result.scalar_one_or_none()

    if not target:
        raise HTTPException(status_code=404, detail="Target not found")

    if target.is_banned:
        raise HTTPException(status_code=403, detail="Target is banned")

    if payload.creator_id == payload.target_id:
        raise HTTPException(
            status_code=400,
            detail="Cannot create challenge for yourself"
        )

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
