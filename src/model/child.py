import enum

from datetime import datetime

from sqlalchemy import Column, VARCHAR, Enum, DateTime
from sqlalchemy.orm import relationship

from src.database import Base
from src.model.unique_constraints import (
    account_unique_constraint, nickname_unique_constraint
)


class ChildType(enum.Enum):
    FIRST: int = 1
    SECOND: int = 2
    THIRD: int = 3
    FORTH: int = 4
    FIFTH: int = 5
    SIXTH: int = 6
    SEVENTH: int = 7
    EIGTHTH: int = 8
    NINTH: int = 9
    TENTH: int = 10


class Child(Base):
    __tablename__: str = "child"
    __table_args__: tuple = (
        account_unique_constraint, nickname_unique_constraint
    )    
    account: str = Column("account", VARCHAR(length=16), nullable=False)
    password: str = Column("password", VARCHAR(length=128), nullable=False)
    nickname: str = Column("nickname", VARCHAR(length=8), nullable=False)
    type: ChildType = Column("type", Enum(ChildType), nullable=False)
    nickname_updated_at: datetime = Column(
        "nickname_updated_at", DateTime(timezone=True), nullable=False
    )
    character_name: str = Column(
        "character_name", VARCHAR(length=8), nullable=False
    )
    character_name_updated_at: datetime = Column(
        "character_name_updated_at", DateTime(timezone=True), nullable=False
    )
    parent = relationship(
        "Parent", secondary="parent_child", back_populates="child"
    )
    question_diary = relationship(
        "QuestionDiary", back_populates="question_diary"
    )
    child_activity_like = relationship(
        "ChildActivityLike", back_populates="child"
    )
    