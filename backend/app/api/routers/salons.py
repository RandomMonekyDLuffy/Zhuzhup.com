from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.salon import SalonOut, ServiceOut
from app.services.salons import get_salon, list_salons, list_services_for_salon

router = APIRouter(prefix="/salons", tags=["salons"])


@router.get("", response_model=list[SalonOut])
def salons(db: Session = Depends(get_db)):
    items = list_salons(db)
    return [
        SalonOut(
            id=s.id,
            name=s.name,
            address=s.address,
            city=s.city,
            description=s.description,
        )
        for s in items
    ]


@router.get("/{salon_id}/services", response_model=list[ServiceOut])
def salon_services(salon_id: int, db: Session = Depends(get_db)):
    salon = get_salon(db, salon_id)
    if not salon:
        raise HTTPException(status_code=404, detail="Salon not found")
    services = list_services_for_salon(db, salon_id)
    return [
        ServiceOut(
            id=svc.id,
            salon_id=svc.salon_id,
            name=svc.name,
            duration_minutes=svc.duration_minutes,
            price=float(svc.price),
        )
        for svc in services
    ]

