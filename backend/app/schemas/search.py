from pydantic import BaseModel


class ServiceMiniOut(BaseModel):
    id: int
    name: str
    duration_minutes: int
    price: float


class ProfessionalSearchResultOut(BaseModel):
    professional_id: int
    professional_name: str
    title: str | None = None
    bio: str | None = None
    salon_id: int
    salon_name: str
    city: str
    services: list[ServiceMiniOut]


class ProfessionalSearchResponseOut(BaseModel):
    location_used: str | None = None
    results: list[ProfessionalSearchResultOut]

