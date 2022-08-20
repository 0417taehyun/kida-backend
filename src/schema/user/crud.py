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
    level: int = 1
    exp_gage: int = 0
    liked: list[dict] | None
    visited: list[dict] | None


class UpdateUser(UserBase):
    child_like: list
    parent_like: list
