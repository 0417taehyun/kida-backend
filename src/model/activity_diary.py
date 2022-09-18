from datetime import datetime

from sqlalchemy import Column, Integer, VARCHAR, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from src.database import Base


class ActivityDiary(Base):
    __tablename__: str = "activity_diary"
    child_activity_like_id: int = Column(
        "child_activity_like_id",
        Integer,
        ForeignKey("child_activity_like.id"),
        nullable=False
    )
    emotion_id: int = Column(
        "emotion_id",
        Integer,
        ForeignKey("emotion.id"),
        nullable=True
    )
    diary_id: int = Column(
        "diary_id",
        Integer,
        ForeignKey("diary.id"),
        nullable=False
    )
    content: str = Column("content", VARCHAR(length=512), nullable=True)
    answered_at: datetime = Column(
        "answered_at", DateTime(timezone=True), nullable=True
    )
    child_activity_like = relationship(
        "ChildActivityLike", back_populates="activity_diary"
    )
    emotion = relationship("Emotion", back_populates="activity_diary")
    activity_diary_reply = relationship(
        "ActivityDiaryReply", back_populates="activity_diary"
    )
    diary = relationship("Diary", back_populates="activity_diary")
    