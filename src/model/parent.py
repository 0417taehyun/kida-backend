import enum

from datetime import datetime

from sqlalchemy import Column, VARCHAR, Enum, DateTime
from sqlalchemy.orm import relationship

from src.database import Base
from src.model.unique_constraints import (
    account_unique_constraint, nickname_unique_constraint
)


class ParentType(str, enum.Enum):
    MOTHER: str = "mother"
    FATHER: str = "father"


class Parent(Base):
    __tablename__: str = "parent"
    __table_args__: tuple = (
        account_unique_constraint, nickname_unique_constraint
    )        
    account: str = Column("account", VARCHAR(length=16), nullable=False)
    password: str = Column("password", VARCHAR(length=128), nullable=False)
    nickname: str = Column("nickname", VARCHAR(length=8), nullable=False)
    type: ParentType = Column("type", Enum(ParentType), nullable=False)
    nickname_updated_at: datetime = Column(
        "nickname_updated_at", DateTime(timezone=True), nullable=False
    )
    invitation_code: str = Column(
        "invitation_code", VARCHAR(length=8), nullable=True
    )
    invication_code_expired_date: datetime = Column(
        "invitation_code_expired_date", DateTime(timezone=True), nullable=True
    )    
    child = relationship(
        "Child", secondary="parent_child", back_populates="parent"
    )
    question_diary = relationship(
        "QuestionDiaryReply",
        secondary="questoin_diary_reply",
        back_populates="parent"
    )
    activity_diary_reply = relationship(
        "ActivityDiaryReply", back_populates="parent"
    )
    parent_activity_like = relationship(
        "ParentActivityLike", back_populates="parent"
    )
    