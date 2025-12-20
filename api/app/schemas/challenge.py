from pydantic import BaseModel
from datetime import datetime

class ChallengeCreate(BaseModel):
    creator_id: int
    target_id: int
    type: str

class ChallengeRead(BaseModel):
    id: int
    creator_id: int
    target_id: int
    type: str
    start_date: datetime
    end_date: datetime | None
    winner_id: int | None

    class Config:
        from_attributes = True
