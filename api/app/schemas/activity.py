from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ActivityBase(BaseModel):
    user_id: int
    type: str = Field(..., description="Тип активности: run, bicycle, swim, workout")
    distance: Optional[float] = None
    duration: Optional[int] = None  # минуты


class ActivityCreate(ActivityBase):
    pass


class ActivityRead(ActivityBase):
    id: int
    points: int
    created_at: datetime

    class Config:
        from_attributes = True
