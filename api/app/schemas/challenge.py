from datetime import date
from typing import Optional

from pydantic import BaseModel


class ChallengeBase(BaseModel):
    creator_id: int
    target_id: int
    type: str
    start_date: date
    end_date: date


class ChallengeCreate(ChallengeBase):
    pass


class ChallengeRead(ChallengeBase):
    id: int
    winner_id: Optional[int] = None

    class Config:
        from_attributes = True
