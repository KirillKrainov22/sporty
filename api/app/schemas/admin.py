from datetime import datetime
from typing import List, Dict, Optional

from pydantic import BaseModel


class AdminUserBanRequest(BaseModel):
    is_banned: bool


class AdminPointsRequest(BaseModel):
    user_id: int
    amount: int
    reason: Optional[str] = None


class AdminUserItem(BaseModel):
    id: int
    telegram_id: int
    username: str | None = None
    points: int
    level: int
    is_banned: bool
    created_at: datetime

    class Config:
        from_attributes = True


class AdminSystemStatistics(BaseModel):
    total_users: int
    active_users_today: int
    total_activities: int
    activities_by_type: Dict[str, int]
    total_points: int
    top_users: List[AdminUserItem]
