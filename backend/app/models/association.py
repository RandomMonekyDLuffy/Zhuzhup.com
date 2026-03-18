from sqlalchemy import Column, ForeignKey, Integer, Table

from app.db.base import Base

professional_services = Table(
    "professional_services",
    Base.metadata,
    Column("professional_id", Integer, ForeignKey("professionals.id"), primary_key=True),
    Column("service_id", Integer, ForeignKey("services.id"), primary_key=True),
)

