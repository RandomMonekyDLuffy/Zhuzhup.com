from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.professional import Professional
from app.models.salon import Salon
from app.models.service import Service
from app.models.user import User, UserRole


def seed_if_empty(db: Session) -> None:
    # Only seed if we don't already have professionals in the DB.
    if db.query(Professional).first():
        return

    # Salons
    s1 = db.query(Salon).filter(Salon.name == "Glow & Go Salon").first()
    if not s1:
        s1 = Salon(
            name="Glow & Go Salon",
            address="12 Market Street",
            city="New York",
            description="Quick appointments, great stylists.",
        )
        db.add(s1)
        db.flush()

    s2 = db.query(Salon).filter(Salon.name == "Urban Shears").first()
    if not s2:
        s2 = Salon(
            name="Urban Shears",
            address="88 Riverside Ave",
            city="New York",
            description="Premium cuts and color specialists.",
        )
        db.add(s2)
        db.flush()

    # Services
    def get_service(salon_id: int, name: str) -> Service | None:
        return db.query(Service).filter(Service.salon_id == salon_id, Service.name == name).first()

    def ensure_service(salon_id: int, name: str, duration_minutes: int, price: float) -> Service:
        svc = get_service(salon_id, name)
        if svc:
            return svc
        svc = Service(salon_id=salon_id, name=name, duration_minutes=duration_minutes, price=price)
        db.add(svc)
        db.flush()
        return svc

    haircut = ensure_service(s1.id, "Haircut", 45, 35.00)
    blow_dry = ensure_service(s1.id, "Blow Dry", 30, 25.00)
    haircut_wash = ensure_service(s2.id, "Haircut + Wash", 60, 55.00)
    color_touch = ensure_service(s2.id, "Color Touch-up", 90, 95.00)

    # Users + professionals
    def ensure_user(email: str, full_name: str) -> User:
        user = db.query(User).filter(User.email == email).first()
        if user:
            return user
        user = User(
            email=email,
            full_name=full_name,
            role=UserRole.professional,
            password_hash=hash_password("Password123!"),
        )
        db.add(user)
        db.flush()
        return user

    def ensure_professional(user: User, salon_id: int, title: str, bio: str) -> Professional:
        prof = db.query(Professional).filter(Professional.user_id == user.id).first()
        if prof:
            return prof
        prof = Professional(user_id=user.id, salon_id=salon_id, title=title, bio=bio)
        db.add(prof)
        db.flush()
        return prof

    ava_user = ensure_user("ava.pro@demo.com", "Ava Johnson")
    mia_user = ensure_user("mia.pro@demo.com", "Mia Chen")
    ben_user = ensure_user("ben.pro@demo.com", "Ben Carter")
    zara_user = ensure_user("zara.pro@demo.com", "Zara Patel")

    ava = ensure_professional(ava_user, s1.id, "Lead Stylist", "Precision cuts + fast blow-dries.")
    mia = ensure_professional(mia_user, s1.id, "Stylist", "Great for everyday hair + styling.")
    ben = ensure_professional(ben_user, s2.id, "Color Specialist", "Color touch-ups + wash-and-style.")
    zara = ensure_professional(zara_user, s2.id, "Senior Stylist", "Blends, highlights, and smooth finishes.")

    # Assign services (avoid duplicates)
    def add_service_if_missing(prof: Professional, svc: Service) -> None:
        existing_ids = {s.id for s in prof.services}
        if svc.id not in existing_ids:
            prof.services.append(svc)

    add_service_if_missing(ava, haircut)
    add_service_if_missing(ava, blow_dry)
    add_service_if_missing(mia, haircut)
    add_service_if_missing(ben, haircut_wash)
    add_service_if_missing(ben, color_touch)
    add_service_if_missing(zara, color_touch)

    db.commit()

