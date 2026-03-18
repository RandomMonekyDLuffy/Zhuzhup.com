from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.schemas.booking import BookingCreate, BookingOut
from app.services.bookings import BookingValidationError, create_booking

router = APIRouter(prefix="/bookings", tags=["bookings"])


@router.post("", response_model=BookingOut, status_code=status.HTTP_201_CREATED)
def create(payload: BookingCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    try:
        booking = create_booking(
            db,
            customer_id=user.id,
            salon_id=payload.salon_id,
            service_id=payload.service_id,
            professional_id=payload.professional_id,
            booking_type=payload.booking_type,
            scheduled_at=payload.scheduled_at,
            is_walk_in_now=payload.is_walk_in_now,
            notes=payload.notes,
        )
    except BookingValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return BookingOut(
        id=booking.id,
        customer_id=booking.customer_id,
        salon_id=booking.salon_id,
        professional_id=booking.professional_id,
        service_id=booking.service_id,
        booking_type=booking.booking_type,
        status=booking.status,
        scheduled_at=booking.scheduled_at,
        is_walk_in_now=booking.is_walk_in_now,
        notes=booking.notes,
        created_at=booking.created_at,
    )

