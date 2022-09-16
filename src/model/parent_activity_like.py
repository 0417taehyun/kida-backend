from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from src.database import Base


class ParentActivityLike(Base):
    __tablename__: str = "parent_activity_like"
    parent_id: int = Column(
        "parent_id", Integer, ForeignKey("parent.id"), nullable=False
    )
    activity_id: int = Column(
        "activity_id", Integer, ForeignKey("activity.id"), nullable=False
    )
    is_visited: bool = Column(
        "is_visited", Boolean, default=False, nullable=False
    )
    parent = relationship("Parent", back_populates="parent_activity")
    activity = relationship("Activity", back_populates="parent_activity")
