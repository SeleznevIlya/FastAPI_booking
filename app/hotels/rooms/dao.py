from datetime import date

from sqlalchemy import and_, func, or_, select

from app.bookings.models import Booking
from app.dao.base import BaseDAO
from app.database import async_session_maker, engine
from app.hotels.rooms.models import Room


class RoomDAO(BaseDAO):
	model = Room

	@classmethod
	async def get_hotel_rooms(cls, hotel_id: int, date_from: date, date_to: date):

		total_days: int = (date_to - date_from).days

		"""
		select r.id, r.hotel_id, r.name, r.quantity,r.quantity-count(b.id), count(b.id)  from public.room as r
		left join public.booking as b on b.room_id = r.id
		where ((b.date_to >= '2023-06-20' and
				b.date_from <= '2023-07-05')or (b.date_to is null and b.date_from is null)) 
				and r.hotel_id = 2
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
							(total_days * Room.price).label('total_price'),
							(Room.quantity - func.count(Booking.id)).label("rooms_left")
							).join(Booking, Booking.room_id == Room.id, isouter=True).\
								where(
									and_(Room.hotel_id == hotel_id,
									or_(
										and_(
											Booking.date_from <= date_to,
											Booking.date_to >= date_from
										),
									  	and_(
											Booking.date_to == None,
											Booking.date_from == None
										)
									)
								)
							).group_by(Room.id)

		# print(hotel_rooms.compile(engine, compile_kwargs={"literal_binds": True}))

		async with async_session_maker() as session:
			result = await session.execute(hotel_rooms)
			return result.all()
