from fastapi import APIRouter
from app.hotels.dao import HotelDAO
from app.hotels.schemas import SHotel
from datetime import date


router = APIRouter(
	prefix="/hotels",
	tags=["Отели"]
)


@router.get("/")
async def get_hotels():
	return await HotelDAO.find_all()


@router.get("/{location}", response_model=list[SHotel])
async def get_hotels_by_location(location: str, date_from: date, date_to: date):
	return await HotelDAO.find_all_by_location(location, date_from, date_to)


@router.get("/{hotel_id}")
async def get_hotels_by_id(hotel_id: int):
	return await HotelDAO.find_by_id(hotel_id)

