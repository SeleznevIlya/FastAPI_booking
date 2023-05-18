from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from sqladmin import Admin, ModelView

from redis import asyncio as aioredis

from app.config import settings
from app.admin.views import UserAdmin, BookingAdmin, HotelAdmin, RoomAdmin
from app.admin.auth import authentication_backend
from app.database import engine
from app.bookings.router import router as router_bookings
from app.auth.router import router as auth_router
from app.hotels.router import router as router_hotels
from app.pages.router import router as router_pages
from app.images.router import router as router_images

app = FastAPI()
admin = Admin(app, engine, authentication_backend=authentication_backend,)

admin.add_view(UserAdmin)
admin.add_view(BookingAdmin)
admin.add_view(HotelAdmin)
admin.add_view(RoomAdmin)

app.mount("/static", StaticFiles(directory="app/static"), "static")

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Authorization"],
)

app.include_router(auth_router)
app.include_router(router_bookings)
app.include_router(router_hotels)
app.include_router(router_pages)
app.include_router(router_images)


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


