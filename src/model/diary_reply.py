import enum

from sqlalchemy import Column, Enum
from sqlalchemy.orm import relationship

from src.database import Base
from src.model.diary import DiaryType


class DiaryReply(Base):
    __tablename__: str = "diary_reply"
    type: enum = Column("type", Enum(DiaryType), nullable=False)
    question_diary_reply = relationship("QuestionDiaryReply", back_populates="diary_reply")
    activity_diary_reply = relationship("ActivityDiaryReply", back_populates="diary_reply")
    