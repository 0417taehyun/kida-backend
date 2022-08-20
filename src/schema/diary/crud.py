from typing import Any
from enum import Enum
from datetime import datetime

from pydantic import BaseModel

from src.schema.question import QuestionKeywords


class DiaryType(str, Enum):
    ANSWER = "answer"
    ACTIVITY = "activity"

class EmotionType(str, Enum):
    """
    종류 다섯 개
    기쁨, 무표정, 놀람, 슬픔, 화남
    """
    HAPPY = "happy"
    ORDINARY = "ordinary"
    SURPRISED = "surprised"
    SAD = "sad"
    ANGRY = "angry"

class DiaryBase(BaseModel):
    pass


class CreateDiary(DiaryBase):
    child_id: Any
    parent_id: Any
    diary_type: DiaryType
    question_id: Any
    sequence_id: int
    question_content: str
    question_keyword: QuestionKeywords
    child_answered_at: datetime | None = None
    parent_answered_at: datetime | None = None
    is_child_read: bool = False
    is_parent_read: bool = False
    is_child_answered: bool = False
    is_parent_answered: bool = False
    

class UpdateDiary(DiaryBase):
    """
    자녀 또는 부모가 답변을 하는 경우
    """
    emotion: EmotionType | None
    answer: str
    
    class Config:
        schema_extra = {
            "example": {
                "emotion": "sad",
                "answer": "예전에 엄마가 학교 앞에서 사준 떡꼬치가 엄청 맛있었는데 오랜만에 먹고 싶다."
            }
        }

    
