import asyncio
from datetime import date, datetime

from fastapi import APIRouter, Query
from fastapi_cache.decorator import cache
from starlette import status

from app.exceptions import BookingLimitExceededException, DateBookingException
from app.hotels.dao import HotelDAO
from app.hotels.rooms.dao import RoomDAO
from app.hotels.rooms.schemas import SRoomPrice
from app.hotels.schemas import SHotel

router = APIRouter(
	prefix="/hotels",
	tags=["Отели"]
)


@router.get("/")
async def get_hotels():
	return await HotelDAO.find_all()


@router.get('/{hotel_id}/rooms')
async def get_hotels_rooms(hotel_id: int,
							date_from: date = Query(..., description=f"Haпpuмep, {datetime.now().date()}"),
							date_to: date = Query(..., description=f"Haпpuмep, {datetime.now().date()}")) -> list[SRoomPrice]:
	if date_from > date_to:
		raise DateBookingException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ошибка ввода: дата заезда не может быть позже даты отъезда",)
	if (date_to - date_from).days > 30:
		raise BookingLimitExceededException(status_code=status.HTTP_400_BAD_REQUEST, detail="Нельзя забронировать комнату более чем на 30 дней",)
	return await RoomDAO.get_hotel_rooms(hotel_id, date_from, date_to)


@router.get("/{location}")
@cache(expire=60)
async def get_hotels_by_location(location: str,
								date_from: date = Query(..., description=f"Haпpuмep, {datetime.now().date()}"),
								date_to: date = Query(..., description=f"Haпpuмep, {datetime.now().date()}")) -> list[SHotel]:
	await asyncio.sleep(3)
	return await HotelDAO.find_all_by_location(location, date_from, date_to)


@router.get("/id/{hotel_id}")
async def get_hotels_by_id(hotel_id: int):
	return await HotelDAO.find_by_id(hotel_id)




