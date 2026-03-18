from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.search import ProfessionalSearchResponseOut
from app.services.search import search_professionals

router = APIRouter(prefix="/search", tags=["search"])


@router.get("/professionals", response_model=ProfessionalSearchResponseOut)
def professionals_search(
    service: Annotated[str, Query(min_length=1, max_length=255)],
    location: Annotated[str | None, Query(default=None, max_length=255)] = None,
    lat: Annotated[float | None, Query(default=None)] = None,
    lng: Annotated[float | None, Query(default=None)] = None,
    db: Session = Depends(get_db),
):
    return search_professionals(
        db,
        service_keyword=service,
        location_keyword=location,
        lat=lat,
        lng=lng,
    )

