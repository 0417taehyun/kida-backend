import enum

from sqlalchemy import Column, Enum
from sqlalchemy.orm import relationship

from src.database import Base


class EmotionType(str, enum.Enum):
    HAPPY = "happy"
    SURPRISED = "surprised"
    ORDINARY = "ordinary"
    SAD = "sad"
    ANGRY = "angry"


class Emotion(Base):
    __tablename__: str = "emotion"
    type: EmotionType = Column("type", Enum(EmotionType), nullable=False)
    question_diary = relationship("QuestionDiary", back_populates="emotion")
    activity_diary = relationship("ActivityDiary", back_populates="emotion")