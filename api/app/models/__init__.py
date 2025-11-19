from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

from .user import User
from .activity import Activity
from .friend import Friend
from .challenge import Challenge
from .achievement import Achievement
