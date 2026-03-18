from fastapi import APIRouter

from app.api.routers import auth, bookings, salons, search

api_router = APIRouter(prefix="/api")
api_router.include_router(auth.router)
api_router.include_router(salons.router)
api_router.include_router(bookings.router)
api_router.include_router(search.router)

