from __future__ import annotations

import enum
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class BookingType(str, enum.Enum):
    scheduled = "scheduled"
    walk_in = "walk_in"


class BookingStatus(str, enum.Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"
    completed = "completed"


class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    customer_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    salon_id: Mapped[int] = mapped_column(ForeignKey("salons.id"), nullable=False, index=True)
    professional_id: Mapped[int | None] = mapped_column(
        ForeignKey("professionals.id"),
        nullable=True,
        index=True,
    )
    service_id: Mapped[int] = mapped_column(ForeignKey("services.id"), nullable=False, index=True)

    booking_type: Mapped[BookingType] = mapped_column(Enum(BookingType), nullable=False)
    status: Mapped[BookingStatus] = mapped_column(Enum(BookingStatus), nullable=False, default=BookingStatus.pending)

    scheduled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    is_walk_in_now: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    notes: Mapped[str | None] = mapped_column(String(1000), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    customer: Mapped["User"] = relationship(back_populates="bookings")
    salon: Mapped["Salon"] = relationship()
    professional: Mapped["Professional"] = relationship(back_populates="bookings")
    service: Mapped["Service"] = relationship(back_populates="bookings")


from app.models.professional import Professional  # noqa: E402
from app.models.salon import Salon  # noqa: E402
from app.models.service import Service  # noqa: E402
from app.models.user import User  # noqa: E402

