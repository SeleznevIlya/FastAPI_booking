from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.hotels.rooms.models import Room
from sqlalchemy import select
from datetime import date


class RoomDAO(BaseDAO):
	model = Room

	@classmethod
	async def get_hotel_rooms(cls, hotel_id: int, date_from: date, date_to: date):

		total_days: int = (date_to - date_from).days

		#print(type(total_days))

		hotel_rooms = select(Room.id, Room.hotel_id, Room.name, (total_days*Room.price).label('total_price')).where(Room.hotel_id == hotel_id)

		async with async_session_maker() as session:
			result = await session.execute(hotel_rooms)
			return result.all()
