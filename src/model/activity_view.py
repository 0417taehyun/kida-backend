from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship

from src.database import Base


class ActivityView(Base):
    __tablename__: str = "activity_view"
    count: int = Column("count", Integer, nullable=False)
    activity = relationship("Activity", back_populates="activity_view")
    