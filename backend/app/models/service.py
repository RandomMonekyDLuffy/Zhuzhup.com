from __future__ import annotations

from sqlalchemy import ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.association import professional_services


class Service(Base):
    __tablename__ = "services"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    salon_id: Mapped[int] = mapped_column(ForeignKey("salons.id"), nullable=False, index=True)

    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    duration_minutes: Mapped[int] = mapped_column(Integer, nullable=False, default=30)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False, default=0)

    salon: Mapped["Salon"] = relationship(back_populates="services")
    professionals: Mapped[list["Professional"]] = relationship(
        secondary=professional_services,
        back_populates="services",
    )
    bookings: Mapped[list["Booking"]] = relationship(back_populates="service")


from app.models.booking import Booking  # noqa: E402
from app.models.professional import Professional  # noqa: E402
from app.models.salon import Salon  # noqa: E402

