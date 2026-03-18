from sqlalchemy.orm import Session

from app.models.salon import Salon
from app.models.service import Service


def list_salons(db: Session) -> list[Salon]:
    return db.query(Salon).order_by(Salon.name.asc()).all()


def get_salon(db: Session, salon_id: int) -> Salon | None:
    return db.query(Salon).filter(Salon.id == salon_id).first()


def list_services_for_salon(db: Session, salon_id: int) -> list[Service]:
    return db.query(Service).filter(Service.salon_id == salon_id).order_by(Service.name.asc()).all()

