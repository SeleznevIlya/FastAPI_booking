from app.dao.base import BaseDAO
from app.bookings.models import Booking
from app.hotels.rooms.models import Room
from datetime import date
from sqlalchemy import select, insert, and_, func
from app.database import engine, async_session_maker


class BookingDAO(BaseDAO):
	model = Booking

	@classmethod
	async def add(cls, user_id: int,
				room_id: int,
				date_from: date,
				date_to: date):
		"""
		WITH booked_rooms AS (
		SELECT * FROM booking
		WHERE room_id = 1 AND
		date_to >= '2023-06-20' and
		date_from <= '2023-07-05'
		)
		"""

		booked_rooms = select(Booking).where(
			and_(Booking.room_id == room_id),
			and_(Booking.date_to >= date_from),
			and_(Booking.date_from <= date_to)).cte("booked_rooms")
		#print(booked_rooms.compile(engine, compile_kwargs={"literal_binds": True}))

		"""
			SELECT room.quantity - COUNT (booked_rooms.room_id) FROM room
			LEFT JOIN booked_rooms ON booked_rooms.room_id = room. id
			WHERE room.id = 1

			GROUP BY room.quantity, booked_rooms.room_id
		"""

		get_rooms_left = select(
			(Room.quantity - func.count(booked_rooms.c.room_id)).label("rooms_left")
			).select_from(Room).join(
			booked_rooms, booked_rooms.c.room_id == Room.id, isouter=True
			).where(Room.id == room_id).group_by(
			Room.quantity, booked_rooms.c.room_id
			)
		#print(get_rooms_left.compile(engine, compile_kwargs={"literal_binds": True}))

		async with async_session_maker() as session:
			rooms_left = await session.execute(get_rooms_left)
			rooms_left: int = rooms_left.scalar()
			
			if rooms_left > 0:
				get_price = select(Room.price).filter_by(id=room_id)
				price = await session.execute(get_price)
				price: int = price.scalar()
				add_booking = insert(Booking).values(
					room_id=room_id,
					user_id=user_id,
					date_from=date_from,
					date_to=date_to,
					price=price,
				).returning(Booking)
				new_booking = await session.execute(add_booking)
				await session.commit()
				return new_booking.scalar()
			else:
				return None

		

