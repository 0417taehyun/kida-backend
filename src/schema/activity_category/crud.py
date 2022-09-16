from pydantic import BaseModel


class BaseActivityCategory(BaseModel):
    name: str


class CreateActivityCategory(BaseActivityCategory):
    
    class Config:
        schema_extra = {
            "examples": {
                "name": "등록하고자 하는 활동 목록 이름"
            }
        }


class UpdaetActivityCategory(BaseActivityCategory):
    
    class Config:
        schema_extra = {
            "examples": {
                "name": "수정하고자 하는 활동 목록 이름"
            }
        }
