from enum import Enum
from pydantic import BaseModel


class UserType(str, Enum):
    CHILD = "child"
    PARENT = "parent"
    

class UserBase(BaseModel):
    pass


class CreateUser(UserBase):
    type: UserType | None
    id: str
    child_id: str | None
    parent_id: str | None
    password: str


class UpdateUser(UserBase):
    pass