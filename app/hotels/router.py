from fastapi import APIRouter
from app.hotels.dao import HotelDAO
from app.hotels.rooms.dao import RoomDAO
from app.hotels.rooms.schemas import SRoom, SRoom_Price
from app.hotels.schemas import SHotel
from datetime import date


router = APIRouter(
	prefix="/hotels",
	tags=["Отели"]
)


@router.get("/")
async def get_hotels():
	return await HotelDAO.find_all()


@router.get('/{hotel_id}/rooms', response_model=list[SRoom_Price])
async def get_hotels_rooms(hotel_id: int, date_from: date, date_to: date):
	return await RoomDAO.get_hotel_rooms(hotel_id, date_from, date_to)
	#return await RoomDAO.find_all(hotel_id=hotel_id)

@router.get("/{location}", response_model=list[SHotel])
async def get_hotels_by_location(location: str, date_from: date, date_to: date):
	return await HotelDAO.find_all_by_location(location, date_from, date_to)


@router.get("/search/{hotel_id}")
async def get_hotels_by_id(hotel_id: int):
	return await HotelDAO.find_by_id(hotel_id)




