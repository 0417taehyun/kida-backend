from enum import Enum

from pydantic import BaseModel


class QuestionKeywords(str, Enum):
    SCHOOL = "school"
    FRIEND = "friend"
    ANXIETY = "anxiety"
    TALENT = "talent"


class QuestionBase(BaseModel):
    pass


class CreateQuestion(QuestionBase):
    content: str
    sequence_id: int 
    keyword: QuestionKeywords
    
    
class UpdateQuestion(QuestionBase):
    pass