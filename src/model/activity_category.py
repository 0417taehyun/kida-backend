from sqlalchemy import Column, VARCHAR
from sqlalchemy.orm import relationship

from src.database import Base


class ActivityCategory(Base):
    __tablename__: str = "activity_category"
    name: str = Column("name", VARCHAR(length=4), nullable=False)
    activity = relationship("Activity", back_populates="activity_category")
    