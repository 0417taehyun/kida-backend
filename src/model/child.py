import enum

from datetime import datetime

from sqlalchemy import Column, VARCHAR, Enum, DateTime, Integer, ForeignKey
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
    experience: int = Column("experience", Integer, default=0, nullable=False)
    level_id: int = Column(
        "level_id",
        Integer,
        ForeignKey(column="level.id"),
        default=1,
        nullable=False
    )    
    nickname_updated_at: datetime = Column(
        "nickname_updated_at", DateTime(timezone=True), nullable=False
    )
    character_name: str = Column(
        "character_name", VARCHAR(length=8), nullable=False
    )
    character_name_updated_at: datetime = Column(
        "character_name_updated_at", DateTime(timezone=True), nullable=False
    )
    invitation_code: str = Column(
        "invitation_code", VARCHAR(length=8), nullable=True
    )
    invication_code_expired_date: datetime = Column(
        "invitation_code_expired_date", DateTime(timezone=True), nullable=True
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
    level = relationship("Level", back_populates="level")
    