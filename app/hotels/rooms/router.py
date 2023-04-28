from app.hotels.rooms.schemas import SRoom
from app.hotels.router import router
from app.hotels.rooms.dao import RoomDAO


@router.get('/{hotel_id}/rooms', response_model=list[SRoom])
async def get_hotels_rooms(hotel_id: int):
	return await RoomDAO.get_hotel_rooms(hotel_id)
