import enum

from sqlalchemy import Column, Enum
from sqlalchemy.orm import relationship

from src.database import Base


class DiaryType(str, enum.Enum):
    ACTIVITY: str = "activity"
    QUESTION: str = "question"


class Diary(Base):
    __tablename__: str = "diary"
    type: enum = Column("type", Enum(DiaryType), nullable=False)
    question_diary = relationship("QuestionDiary", back_populates="diary")
    activity_diary = relationship("ActivityDiary", back_populates="diary")
    question_diary_reply = relationship("QuestionDiaryReply", back_populates="diary")
    activity_diary_reply = relationship("ActivityDiaryReply", back_populates="diary")
    