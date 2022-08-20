from pydantic import BaseModel


class QuestionBase(BaseModel):
    pass


class CreateQuestion(QuestionBase):
    content: str
    
    
class UpdateQuestion(QuestionBase):
    pass