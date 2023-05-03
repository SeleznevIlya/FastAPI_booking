from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.bookings.router import router as router_bookings
from app.auth.router import router as auth_router
from app.hotels.router import router as router_hotels
from app.pages.router import router as router_pages
from app.images.router import router as router_images

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), "static")

app.include_router(auth_router)
app.include_router(router_bookings)
app.include_router(router_hotels)
app.include_router(router_pages)
app.include_router(router_images)
