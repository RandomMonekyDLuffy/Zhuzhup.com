from __future__ import annotations

import httpx
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.association import professional_services
from app.models.professional import Professional
from app.models.salon import Salon
from app.models.service import Service
from app.models.user import User
from app.schemas.search import (
    ProfessionalSearchResponseOut,
    ProfessionalSearchResultOut,
    ServiceMiniOut,
)


def _reverse_geocode_city(lat: float, lng: float) -> str | None:
    # MVP: use OpenStreetMap Nominatim reverse geocoding to get a city/town name.
    # For production, consider adding caching + a proper geocoding provider.
    url = "https://nominatim.openstreetmap.org/reverse"
    params = {"format": "jsonv2", "lat": lat, "lon": lng}
    headers = {
        # Nominatim requires a valid User-Agent string.
        "User-Agent": "SalonAggregator/1.0 (FastAPI demo)",
    }
    try:
        r = httpx.get(url, params=params, headers=headers, timeout=10)
        r.raise_for_status()
        data = r.json()
    except Exception:
        return None

    address = (data or {}).get("address") or {}
    # Prefer the most specific available field.
    return (
        address.get("city")
        or address.get("town")
        or address.get("village")
        or address.get("hamlet")
        or address.get("county")
    )


def search_professionals(
    db: Session,
    *,
    service_keyword: str,
    location_keyword: str | None,
    lat: float | None,
    lng: float | None,
) -> ProfessionalSearchResponseOut:
    service_keyword = (service_keyword or "").strip()
    if not service_keyword:
        # Keep this simple for now; frontend always supplies it.
        return ProfessionalSearchResponseOut(location_used=location_keyword, results=[])

    city_used = (location_keyword or "").strip() or None
    if not city_used and lat is not None and lng is not None:
        city_used = _reverse_geocode_city(lat, lng)

    service_kw = f"%{service_keyword}%"
    city_frags: list[str] = []
    if city_used:
        city_frags.append(city_used.strip())
        # Common reverse-geocode output like "New York City" won't match our stored "New York".
        normalized = city_used.strip()
        if normalized.lower().endswith(" city"):
            normalized = normalized[: -len(" city")]
        city_frags.append(normalized.strip())
        city_frags = [c for c in dict.fromkeys(city_frags) if c]

    # Query all professionals who offer services matching service_keyword,
    # and whose salon city matches location (if location is provided).
    q = (
        db.query(Professional, User, Salon, Service)
        .join(professional_services, professional_services.c.professional_id == Professional.id)
        .join(Service, Service.id == professional_services.c.service_id)
        .join(User, User.id == Professional.user_id)
        .join(Salon, Salon.id == Professional.salon_id)
        .filter(Service.name.ilike(service_kw))
    )
    if city_frags:
        q = q.filter(
            or_(*[Salon.city.ilike(f"%{frag}%") for frag in city_frags if frag])
        )

    rows = q.all()

    by_prof: dict[int, ProfessionalSearchResultOut] = {}
    for prof, user, salon, service in rows:
        if prof.id not in by_prof:
            by_prof[prof.id] = ProfessionalSearchResultOut(
                professional_id=prof.id,
                professional_name=user.full_name,
                title=prof.title,
                bio=prof.bio,
                salon_id=salon.id,
                salon_name=salon.name,
                city=salon.city,
                services=[],
            )

        # Avoid duplicates (same professional/service combination can appear more than once).
        existing_service_ids = {s.id for s in by_prof[prof.id].services}
        if service.id not in existing_service_ids:
            by_prof[prof.id].services.append(
                ServiceMiniOut(
                    id=service.id,
                    name=service.name,
                    duration_minutes=service.duration_minutes,
                    price=float(service.price),
                )
            )

    results = list(by_prof.values())
    # Sort by number of matching services (descending), then name.
    results.sort(key=lambda r: (-len(r.services), r.professional_name.lower()))

    return ProfessionalSearchResponseOut(location_used=city_used, results=results)

