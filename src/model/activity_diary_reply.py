from datetime import datetime

from sqlalchemy import Column, Integer, VARCHAR, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from src.database import Base


class ActivityDiaryReply(Base):
    __tablename__: str = "activity_diary_reply"
    parent_id: int = Column(
        "parent_id",
        Integer,
        ForeignKey("parent.id"),
        nullable=False
    )
    activity_diary_id: int = Column(
        "activity_diary_id",
        Integer,
        ForeignKey("activity_diary.id"),
        nullable=False
    )
    content: str = Column("content", VARCHAR(length=512), nullable=False)
    answered_at: datetime = Column(
        "answered_at", DateTime(timezone=True), nullable=False
    )
    parent = relationship("Parent", back_populates="activity_diary_reply")
    activity_diary = relationship("ActivityDiary", back_populates="activity_diary_reply")
    