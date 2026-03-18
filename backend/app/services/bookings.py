from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.booking import Booking, BookingType
from app.models.salon import Salon
from app.models.service import Service


class BookingValidationError(ValueError):
    pass


def create_booking(
    db: Session,
    *,
    customer_id: int,
    salon_id: int,
    service_id: int,
    professional_id: int | None,
    booking_type: BookingType,
    scheduled_at: datetime | None,
    is_walk_in_now: bool,
    notes: str | None,
) -> Booking:
    salon = db.query(Salon).filter(Salon.id == salon_id).first()
    if not salon:
        raise BookingValidationError("Salon not found")

    service = db.query(Service).filter(Service.id == service_id, Service.salon_id == salon_id).first()
    if not service:
        raise BookingValidationError("Service not found for this salon")

    if booking_type == BookingType.scheduled:
        if not scheduled_at:
            raise BookingValidationError("scheduled_at is required for scheduled bookings")
        if scheduled_at.tzinfo is None:
            raise BookingValidationError("scheduled_at must be timezone-aware (e.g. 2026-03-18T10:00:00Z)")
        if scheduled_at < datetime.now(timezone.utc):
            raise BookingValidationError("scheduled_at must be in the future")
        is_walk_in_now = False
    else:
        scheduled_at = None
        is_walk_in_now = True if is_walk_in_now is False else is_walk_in_now

    booking = Booking(
        customer_id=customer_id,
        salon_id=salon_id,
        professional_id=professional_id,
        service_id=service_id,
        booking_type=booking_type,
        scheduled_at=scheduled_at,
        is_walk_in_now=is_walk_in_now,
        notes=notes,
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking

