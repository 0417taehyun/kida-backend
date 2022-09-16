from pydantic import BaseModel, HttpUrl, validator

from src.model import LevelType


class BaseLevel(BaseModel):
    pass


class CreateLevel(BaseLevel):
    required_experience: str
    ordinary_character_image_url: HttpUrl
    child_to_parent_character_image_url: HttpUrl
    parent_to_child_character_image_url: HttpUrl


    @validator("required_experience")
    def convert_required_experience(cls, value: str) -> str:
        enum_values: list[str] = [ enum.name for enum in LevelType ]        
        if value in enum_values:
            return value
        
        else:
            raise ValueError(
                "level must be LEVEL_1, LEVEL2, LEVEL_3 or LEVEL_4"
           )
        