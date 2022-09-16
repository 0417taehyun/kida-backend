from datetime import datetime

from sqlalchemy import Column, Integer, VARCHAR, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from src.database import Base


class QuestionDiary(Base):
    __tablename__: str = "question_diary"
    child_id: int = Column(
        "child_id", Integer, ForeignKey("child.id"), nullable=False
    )
    question_id: int = Column(
        "question_id", Integer, ForeignKey("question.id"), nullable=False
    )
    emotion_id: int = Column(
        "emotion_id", Integer, ForeignKey("emotion.id"), nullable=True
    )
    content: str = Column("content", VARCHAR(length=512), nullable=True)
    answered_at: datetime = Column(
        "answered_at", DateTime(timezone=True), nullable=True
    )
    child = relationship("Child", back_populates="question_diary")
    question = relationship("Question", back_populates="question_diary")
    emotion = relationship("Emotion", back_populates="question_diary")
    question_diary_reply = relationship(
        "QuestionDiaryReply", back_populates="question_diary"
    )
    