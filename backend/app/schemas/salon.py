from pydantic import BaseModel


class SalonOut(BaseModel):
    id: int
    name: str
    address: str
    city: str
    description: str | None = None


class ServiceOut(BaseModel):
    id: int
    salon_id: int
    name: str
    duration_minutes: int
    price: float

