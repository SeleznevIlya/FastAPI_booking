from fastapi import APIRouter, Query
from app.hotels.dao import HotelDAO
from app.hotels.rooms.dao import RoomDAO
from app.hotels.rooms.schemas import SRoom, SRoomPrice
from app.hotels.schemas import SHotel
from datetime import date, datetime


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
	return await RoomDAO.get_hotel_rooms(hotel_id, date_from, date_to)


@router.get("/{location}")
async def get_hotels_by_location(location: str,
								date_from: date = Query(..., description=f"Haпpuмep, {datetime.now().date()}"),
								date_to: date = Query(..., description=f"Haпpuмep, {datetime.now().date()}")) -> list[SHotel]:
	return await HotelDAO.find_all_by_location(location, date_from, date_to)


@router.get("/id/{hotel_id}")
async def get_hotels_by_id(hotel_id: int):
	return await HotelDAO.find_by_id(hotel_id)




