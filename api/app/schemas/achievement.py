from datetime import datetime

from pydantic import BaseModel


class AchievementBase(BaseModel):
    user_id: int
    achievement_type: str


class AchievementRead(AchievementBase):
    id: int
    earned_at: datetime

    class Config:
        from_attributes = True
