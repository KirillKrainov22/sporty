from pydantic import BaseModel

class LeaderboardUser(BaseModel):
    user_id: int
    username: str
    points: int

    class Config:
        from_attributes = True
