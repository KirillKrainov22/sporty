from typing import List, Optional
from datetime import datetime, date
from pydantic import BaseModel

# ----- Схема для создания пользователя -----
class UserCreate(BaseModel):
    telegram_id: int
    username: str | None = None


# ----- Схема для ответа пользователя -----
class UserRead(BaseModel):
    id: int
    telegram_id: int
    username: str | None = None
    points: int
    level: int
    created_at: datetime


    class Config:
        orm_mode = True


class DailyProgress(BaseModel):
    date: date
    points: int


class WeeklyProgress(BaseModel):
    week_start: date
    points: int


class ActivityTypeStats(BaseModel):
    type: str
    count: int
    distance: float
    duration: int


class UserStats(BaseModel):
    user_id: int
    username: str
    points: int
    level: int

    total_activities: int
    total_distance: float
    total_duration: int

    global_rank: int

    daily_progress: List[dict]
    weekly_progress: List[dict]
    activity_type_stats: List[dict]

    class Config:
        from_attributes = True


class AdminUserRead(UserRead):
    is_banned: bool
    ban_reason: str | None
    banned_at: datetime | None