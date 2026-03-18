from sqlalchemy.orm import Session

from app.models.salon import Salon
from app.models.service import Service


def seed_if_empty(db: Session) -> None:
    existing = db.query(Salon).first()
    if existing:
        return

    s1 = Salon(
        name="Glow & Go Salon",
        address="12 Market Street",
        city="New York",
        description="Quick appointments, great stylists.",
    )
    s2 = Salon(
        name="Urban Shears",
        address="88 Riverside Ave",
        city="New York",
        description="Premium cuts and color specialists.",
    )

    db.add_all([s1, s2])
    db.flush()

    services = [
        Service(salon_id=s1.id, name="Haircut", duration_minutes=45, price=35.00),
        Service(salon_id=s1.id, name="Blow Dry", duration_minutes=30, price=25.00),
        Service(salon_id=s2.id, name="Haircut + Wash", duration_minutes=60, price=55.00),
        Service(salon_id=s2.id, name="Color Touch-up", duration_minutes=90, price=95.00),
    ]
    db.add_all(services)
    db.commit()

