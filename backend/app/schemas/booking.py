from datetime import datetime

from pydantic import BaseModel, Field

from app.models.booking import BookingStatus, BookingType


class BookingCreate(BaseModel):
    salon_id: int
    service_id: int
    professional_id: int | None = None
    booking_type: BookingType
    scheduled_at: datetime | None = None
    is_walk_in_now: bool = False
    notes: str | None = Field(default=None, max_length=1000)


class BookingOut(BaseModel):
    id: int
    customer_id: int
    salon_id: int
    professional_id: int | None
    service_id: int
    booking_type: BookingType
    status: BookingStatus
    scheduled_at: datetime | None
    is_walk_in_now: bool
    notes: str | None
    created_at: datetime

