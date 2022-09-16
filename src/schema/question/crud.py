from pydantic import BaseModel


class BaseQuestion(BaseModel):
    content: str


class CreateQuestion(BaseQuestion):
    question_category_id: int
    
    class Config:
        schema_extra = {
            "example": {
                "question_category_id": 1,
                "content": "질문 내용"
            }
        }


class UpdateQuestion(BaseQuestion):
    class Config:
        schema_extra = {
            "example": {
                "content": "수정하려는 내용"
            }
        }
