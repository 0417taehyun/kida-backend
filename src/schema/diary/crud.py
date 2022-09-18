from enum import Enum

from pydantic import BaseModel


class DiaryType(str, Enum):
    DIARY: str = "diary"
    REPLY: str = "reply"


class BaseDiary(BaseModel):
    content: str | None
    emotion_id: int | None


class CreateDiary(BaseDiary):
    content: str
    emotion_id: int


class UpdateDiary(BaseDiary):
    pass
