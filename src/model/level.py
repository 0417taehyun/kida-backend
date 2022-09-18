import enum

from pydantic import HttpUrl
from sqlalchemy import Column, Enum, VARCHAR
from sqlalchemy.orm import relationship

from src.database import Base


class LevelType(enum.Enum):
    LEVEL_1: int = 1000
    LEVEL_2: int = 5000
    LEVEL_3: int = 10000
    LEVEL_4: int = 20000


class Level(Base):
    __tablename__: LevelType = "level"
    required_experience: LevelType = Column(
        "required_experience", Enum(LevelType), nullable=False
    )
    ordinary_character_image_url: HttpUrl = Column(
        "ordinary_character_image_url", VARCHAR(length=1024), nullable=False
    )
    child_to_parent_character_image_url: HttpUrl = Column(
        "child_to_parent_character_image_url",
        VARCHAR(length=1024),
        nullable=False
    )
    parent_to_child_character_image_url: HttpUrl = Column(
        "parent_to_child_character_image_url",
        VARCHAR(length=1024),
        nullable=False
    )        
    child = relationship("Child", back_populates="level")
    