from datetime import datetime

from pydantic import BaseModel



class AchievementStatus(BaseModel):
    code: str
    title: str
    earned: bool

    class Config:
        from_attributes = True
