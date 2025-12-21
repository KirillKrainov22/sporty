from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db import get_session
from app.models.user import User
from app.models.achievement import Achievement
from app.schemas.achievement import AchievementStatus

router = APIRouter(
    prefix="/api/users",
    tags=["Achievements"]
)


@router.get("/{user_id}/achievements", response_model=list[AchievementStatus])
async def get_user_achievements(
    user_id: int,
    db: AsyncSession = Depends(get_session)
):
    # 1. Проверяем пользователя
    user = await db.get(User, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.is_banned:
        raise HTTPException(status_code=403, detail="User is banned")

    # 2. ВСЕ возможные достижения (пока захардкодили)
    ALL_ACHIEVEMENTS = [
        {"code": "first_run", "title": "Первый забег"},
        {"code": "100km_month", "title": "Марафонец (100 км за месяц)"},
    ]

    # 3. Какие достижения получены пользователем
    result = await db.execute(
        select(Achievement.code).where(Achievement.user_id == user_id)
    )
    earned_codes = {row[0] for row in result.all()}

    # 4. Формируем ответ для бота
    response = []

    for ach in ALL_ACHIEVEMENTS:
        response.append({
            "code": ach["code"],
            "title": ach["title"],
            "earned": ach["code"] in earned_codes
        })

    return response
