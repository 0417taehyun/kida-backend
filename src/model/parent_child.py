from datetime import datetime

from sqlalchemy import Column, Integer, VARCHAR, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from src.database import Base


class ParentChild(Base):
    __tablename__: str = "parent_child"
    parent_id: int = Column(
        "parent_id",
        Integer,
        ForeignKey(column="parent.id"),
        nullable=True
    )
    child_id: int  = Column(
        "child_id",
        Integer,
        ForeignKey(column="child.id"),
        nullable=True
    )
    invitation_code: str = Column(
        "invitation_code", VARCHAR(length=8), nullable=False
    )    
    family = relationship("Family", back_populates="parent_child")
    