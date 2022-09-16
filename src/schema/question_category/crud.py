from pydantic import BaseModel


class BaseQuestionCategory(BaseModel):
    name: str


class CreateQuestionCategory(BaseQuestionCategory):
    class Config:
        schema_extra = {
            "example": {
                "name": "질문 카테고리 제목"
            }
        }
           

class UpdateQuestionCategory(BaseQuestionCategory):
    class Config:
        schema_extra = {
            "example": {
                "name": "수정하려는 질문 카테고리 제목"
            }
        }
