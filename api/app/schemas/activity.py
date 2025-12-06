from pydantic import BaseModel
from datetime import datetime

class ActivityBase(BaseModel):
    user_id: int
    type: str
    distance: float | None = None
    duration: int | None = None

class ActivityCreate(ActivityBase):
    pass

class ActivityRead(ActivityBase):
    id: int
    points: int
    created_at: datetime

    class Config:
        from_attributes = True
