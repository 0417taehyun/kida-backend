import enum

from pydantic import BaseModel, validator

from src.model import ParentType, ChildType

class UserType(str, enum.Enum):
    CHILD: str = "child"
    PARENT: str = "parent"


class BaseUser(BaseModel):
    pass


class GetUser(BaseUser):
    account: str
    password: str
    
    class Config:
        schema_extra = {
            "example": {
                "account": "account",
                "password": "password"
            }
        }


class CreateUser(GetUser):
    type: ParentType | ChildType
    user_type: UserType
    account: str
    password: str
    nickname: str
    character_name: str | None
    
    @validator("nickname")
    def validate_nickname_length(cls, value: str) -> str:
        if len(value) >= 1 and len(value) <= 8:
            return value
        else:
            raise ValueError("nickname must be between 1 and 8")
        
    
    class Config:
        schema_extra = {
            "example": {
                "type": "mother",
                "user_type": "parent",
                "account": "parentId",
                "password": "parentPassword",
                "nickname": "nickname"
            }
        }
    
    
class UpdateUser(BaseUser):
    pass
