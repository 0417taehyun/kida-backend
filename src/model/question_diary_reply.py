from datetime import datetime

from sqlalchemy import Column, Integer, VARCHAR, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from src.database import Base


class QuestionDiaryReply(Base):
    __tablename__: str = "question_diary_reply"
    parent_id: int = Column(
        "parent_id", Integer, ForeignKey("parent.id"), nullable=False
    )
    question_diary_id: int = Column(
        "question_diary_id", Integer, ForeignKey("question_diary.id"), nullable=False
    )
    content: str = Column("content", VARCHAR(length=512), nullable=False)
    answered_at: datetime = Column(
        "answered_at", DateTime(timezone=True), nullable=False
    )
    parent = relationship("Parent", back_populates="question_diary_reply")
    question_diary = relationship("QuestionDiary", back_populates="question_diary_reply")
    