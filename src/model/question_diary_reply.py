from datetime import datetime

from sqlalchemy import Column, Integer, VARCHAR, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from src.database import Base


class QuestionDiaryReply(Base):
    __tablename__: str = "question_diary_reply"
    parent_id: int = Column(
        "parent_id", Integer, ForeignKey("parent.id"), nullable=False
    )
    diary_id: int = Column(
        "diary_id", Integer, ForeignKey("diary.id"), nullable=False
    )     
    content: str = Column("content", VARCHAR(length=512), nullable=False)
    answered_at: datetime = Column(
        "answered_at", DateTime(timezone=True), nullable=False
    )
    parent = relationship("Parent", back_populates="question_diary_reply")
    diary = relationship("Diary", back_populates="question_diary_reply")