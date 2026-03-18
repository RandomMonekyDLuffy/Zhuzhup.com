from __future__ import annotations

import enum
from datetime import datetime

from sqlalchemy import DateTime, Enum, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class UserRole(str, enum.Enum):
    customer = "customer"
    professional = "professional"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    professional_profile: Mapped["Professional"] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        uselist=False,
    )
    bookings: Mapped[list["Booking"]] = relationship(back_populates="customer")


from app.models.booking import Booking  # noqa: E402
from app.models.professional import Professional  # noqa: E402

