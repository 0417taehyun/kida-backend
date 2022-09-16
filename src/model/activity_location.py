from sqlalchemy import Column, VARCHAR
from sqlalchemy.orm import relationship

from src.database import Base


class ActivityLocation(Base):
    __tablename__: str = "activity_location"
    name: str = Column("name", VARCHAR(length=8), nullable=False)
    activity = relationship("Activity", back_populates="activity_location")
    