from fastapi import APIRouter
from app.hotels.dao import HotelDAO
from app.hotels.schemas import SHotel


router = APIRouter(
	prefix="/hotels",
	tags=["Отели"]
)


@router.get("/")
async def get_hotels():
	return await HotelDAO.find_all()


@router.get("/{hotel_id}")
async def get_hotels_by_id(hotel_id: int):
	return await HotelDAO.find_by_id(hotel_id)


@router.get("/{location}",)
async def get_hotels_by_location(location: str):
	return await HotelDAO.find_all_by_location(location)







