from datetime import datetime

from pydantic import BaseModel

from src.model import PaymentType


class BaseActivity(BaseModel):
    title: str | None
    payment: PaymentType | None
    place: str | None
    target: str | None
    page_url: str | None
    image_url: str | None
    reservation_start_date: datetime | None
    reservation_end_date: datetime | None
    event_start_date: datetime | None
    event_end_date: datetime | None
    geo_location_x: float | None
    get_location_y: float | None


class CreateActivity(BaseActivity):
    title: str
    payment: PaymentType
    page_url: str
    
    class Config:
        schema_extra = {
            
        }


class UpdaetActivity(BaseActivity):
    
    class Config:
        schema_extra = {
            
        }
