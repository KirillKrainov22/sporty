from pydantic import BaseModel

class FriendCreate(BaseModel):
    user_id: int
    friend_id: int


class FriendRead(BaseModel):
    id: int
    user_id: int
    friend_id: int
    status: str

    model_config = {"from_attributes": True}
