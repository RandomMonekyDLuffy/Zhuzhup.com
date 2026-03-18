from __future__ import annotations

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.association import professional_services


class Professional(Base):
    __tablename__ = "professionals"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True, nullable=False)
    salon_id: Mapped[int] = mapped_column(ForeignKey("salons.id"), nullable=False, index=True)

    title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    bio: Mapped[str | None] = mapped_column(String(1000), nullable=True)

    user: Mapped["User"] = relationship(back_populates="professional_profile")
    salon: Mapped["Salon"] = relationship(back_populates="professionals")
    services: Mapped[list["Service"]] = relationship(
        secondary=professional_services,
        back_populates="professionals",
    )
    bookings: Mapped[list["Booking"]] = relationship(back_populates="professional")


from app.models.booking import Booking  # noqa: E402
from app.models.user import User  # noqa: E402
from app.models.salon import Salon  # noqa: E402
from app.models.service import Service  # noqa: E402

