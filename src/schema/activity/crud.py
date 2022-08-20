from enum import Enum
from datetime import datetime

from pydantic import BaseModel, HttpUrl


class PaymentType(str, Enum):
    FREE = "free"
    PAID = "paid"

class ActivityBase(BaseModel):
    pass


class CreateActivity(ActivityBase):
    title: str
    type: str
    state: str
    payment: str
    location: str
    reservation_start_date: datetime
    reservation_end_date: datetime
    event_start_date: datetime
    event_end_date: datetime
    image_url: HttpUrl
    page_url: HttpUrl
    target: str
    geo_location_x: float
    geo_location_y: float


class UpdateActivity(ActivityBase):
    pass
    