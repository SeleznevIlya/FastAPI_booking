from app.bookings.models import Booking
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.hotels.rooms.models import Room
from sqlalchemy import select, and_, func
from datetime import date
from app.database import engine


class RoomDAO(BaseDAO):
	model = Room

	@classmethod
	async def get_hotel_rooms(cls, hotel_id: int, date_from: date, date_to: date):

		total_days: int = (date_to - date_from).days

		"""
		select r.id, r.hotel_id, r.name, r.quantity,r.quantity-count(b.id), count(b.id)  from public.room as r
		left join public.booking as b on r.id = b.room_id
		where b.date_to >= '2023-06-20' and
				b.date_from <= '2023-07-05' and r.hotel_id = 6
		group by r.id;
		"""

		hotel_rooms = select(Room.id,
							Room.hotel_id,
							Room.name,
							Room.description,
							Room.services,
							Room.price,
							Room.quantity,
							Room.image_id,
							(total_days*Room.price).label('total_price'),
							(Room.quantity - func.count(Booking.id)).label("rooms_left")
							).join(Booking, Booking.room_id == Room.id, isouter=True).\
								where(and_(Booking.date_to >= date_from),
									and_(Booking.date_from <= date_to),
									  and_(Room.hotel_id == hotel_id)).group_by(Room.id)

		# print(hotel_rooms.compile(engine, compile_kwargs={"literal_binds": True}))

		async with async_session_maker() as session:
			result = await session.execute(hotel_rooms)
			return result.all()
