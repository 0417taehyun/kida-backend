from enum import Enum
from datetime import datetime

from pydantic import BaseModel


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
    child_id: str
    parent_id: str
    question_id: str
    question_content: str
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

    
