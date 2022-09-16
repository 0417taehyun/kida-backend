import enum

from datetime import datetime

from sqlalchemy import (
    Column, Integer, Float, VARCHAR, DateTime, Enum, ForeignKey
)
from sqlalchemy.orm import relationship

from src.database import Base


class PaymentType(str, enum.Enum):
    COST: str = "cost"
    FREE: str = "free"


class Activity(Base):
    __tablename__: str = "activity"
    activity_category_id: int = Column(
        "activity_category_id",
        Integer,
        ForeignKey("activity_category.id"),
        nullable=False
    )
    activity_location_id: int = Column(
        "activity_location_id",
        Integer,
        ForeignKey("activity_location.id"),
        nullable=False
    )
    title: str = Column(
        "title", VARCHAR(length=64), nullable=False
    )
    payment: PaymentType = Column(
        "payment", Enum(PaymentType), nullable=False
    )
    page_url: str = Column("page_url", VARCHAR(length=512), nullable=False)    
    place: str = Column(
        "place", VARCHAR(length=64), nullable=True
    )    
    reservation_start_date: datetime = Column(
        "reservation_start_date", DateTime(timezone=True), nullable=True
    )
    reservation_end_date: datetime = Column(
        "reservation_end_date", DateTime(timezone=True), nullable=True
    )
    event_start_date: datetime = Column(
        "event_start_date", DateTime(timezone=True), nullable=True
    )
    event_end_date: datetime = Column(
        "event_end_date", DateTime(timezone=True), nullable=True
    )
    target: str = Column("target", VARCHAR(length=64), nullable=True)
    image_url: str = Column("image_url", VARCHAR(length=512), nullable=True)
    geo_location_x: float = Column("geo_location_x", Float, nullable=True)
    geo_location_y: float = Column("geo_location_y", Float, nullable=True)
    activity_view = relationship("ActivityView", back_populates="activity")
    activity_category = relationship("ActivityCategory", back_populates="activity")
    activity_location = relationship("ActivityLocation", back_populates="activity")
    child_activity_like = relationship("ChildActivityLike", back_populates="activity")
    parent_activity_like = relationship("ParentActivityLike", back_populates="activity")
    