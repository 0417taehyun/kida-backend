from pydantic import BaseModel

from src.model import EmotionType


class BaseEmotion(BaseModel):
    type: EmotionType


class CreateEmotion(BaseEmotion):
    
    class Config:
        schema_extra = {
            "example": {
                "type": "생성하려는 감정 종류"
            }
        }
    

class UpdaetEmotion(BaseEmotion):

    class Config:
        schema_extra = {
            "example": {
                "type": "수정하려는 감정 종류"
            }
        }
        