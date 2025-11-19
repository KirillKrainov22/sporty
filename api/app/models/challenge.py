from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from . import Base


class Challenge(Base):
    __tablename__ = "challenges"

    id = Column(Integer, primary_key=True)
    creator_id = Column(Integer, ForeignKey("users.id"))
    target_id = Column(Integer, ForeignKey("users.id"))

    type = Column(String)
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime, nullable=True)

    winner_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    creator = relationship("User", back_populates="challenges_created", foreign_keys=[creator_id])
    target = relationship("User", back_populates="challenges_target", foreign_keys=[target_id])
