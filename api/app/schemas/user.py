from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    telegram_id: int
    username: Optional[str] = None


class UserCreate(UserBase):
    """Данные, которые придут при первой регистрации пользователя из бота"""
    pass


class UserRead(UserBase):
    id: int
    created_at: datetime
    points: int
    level: int

    class Config:
        from_attributes = True  # для работы с ORM-моделью


class UserStats(BaseModel):
    user_id: int
    total_points: int
    total_activities: int
    total_distance: float
    total_duration: int  # минуты
