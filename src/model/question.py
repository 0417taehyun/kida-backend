from sqlalchemy import Column, Integer, VARCHAR, ForeignKey
from sqlalchemy.orm import relationship

from src.database import Base


class Question(Base):
    __tablename__: str = "question"
    question_category_id: int = Column(
        "question_category_id",
        Integer,
        ForeignKey("question_category.id"),
        nullable=False
    )
    content: str = Column(
        "content",
        VARCHAR(length=64),
        nullable=False
    )
    question_category = relationship(
        "QuestionCategory", back_populates="question"
    )
    question_diary = relationship("QuestionDiary", back_populates="question")
    