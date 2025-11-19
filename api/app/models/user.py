from sqlalchemy import Column, Integer, String, BigInteger, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from . import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(BigInteger, unique=True, index=True)
    username = Column(String, nullable=True)

    points = Column(Integer, default=0)
    level = Column(Integer, default=1)

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    activities = relationship("Activity", back_populates="user")
    achievements = relationship("Achievement", back_populates="user")
    friends = relationship("Friend", back_populates="user", foreign_keys="Friend.user_id")
    friends_of = relationship("Friend", back_populates="friend", foreign_keys="Friend.friend_id")
    challenges_created = relationship("Challenge", back_populates="creator", foreign_keys="Challenge.creator_id")
    challenges_target = relationship("Challenge", back_populates="target", foreign_keys="Challenge.target_id")
