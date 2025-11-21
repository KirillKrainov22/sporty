from pydantic import BaseModel


class FriendBase(BaseModel):
    user_id: int
    friend_id: int
    status: str = "pending"  # pending / accepted / rejected и т.п.


class FriendCreate(FriendBase):
    pass


class FriendRead(FriendBase):
    id: int

    class Config:
        from_attributes = True
