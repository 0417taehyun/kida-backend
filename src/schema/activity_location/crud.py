from pydantic import BaseModel


class BaseActivityLocation(BaseModel):
    name: str


class CreateActivityLocation(BaseActivityLocation):
    
    class Config:
        schema_extra = {
            "examples": {
                "name": "등록하고자 하는 활동 지역 이름"
            }
        }


class UpdaetActivityLocation(BaseActivityLocation):
    
    class Config:
        schema_extra = {
            "examples": {
                "name": "수정하고자 하는 활동 지역 이름"
            }
        }
