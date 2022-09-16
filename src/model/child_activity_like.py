from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from src.database import Base


class ChildActivityLike(Base):
    __tablename__: str = "child_activity_like"
    child_id: int = Column(
        "child_id", Integer, ForeignKey("child.id"), nullable=False
    )
    activity_id: int = Column(
        "activity_id", Integer, ForeignKey("activity.id"), nullable=False
    )
    is_visited: bool = Column(
        "is_visited", Boolean, default=False, nullable=False
    )
    child = relationship("Child", back_populates="child_activity")
    activity = relationship("Activity", back_populates="child_activity")
