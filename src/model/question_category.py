from sqlalchemy import Column, VARCHAR
from sqlalchemy.orm import relationship

from src.database import Base


class QuestionCategory(Base):
    __tablename__: str = "question_category"
    name: str = Column("name", VARCHAR(length=4), nullable=False)
    question = relationship("Question", back_populates="question_category")
    