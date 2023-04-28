from app.bookings.models import Booking
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.hotels.models import Hotel
from sqlalchemy import select, and_, func
from datetime import date

from app.hotels.rooms.models import Room


class HotelDAO(BaseDAO):
	model = Hotel

	@classmethod
	async def find_all_by_location(cls, location: str, date_from: date, date_to: date):
		"""
				with booked_hotel_rooms as
				(select * from public.booking as b
				left join public.room as r on b.room_id = r.id
				where
				b.date_to >= '2023-06-20' and
				b.date_from <= '2023-07-05')

				select h.name, h.location, h.room_quantity - count(bhr.hotel_id) from public.hotel as h
				left join booked_hotel_rooms as bhr on bhr.hotel_id = h.id
				where h.location like '%Алтай%'
				group by h.name, h.location, h.room_quantity, bhr.hotel_id;
		"""

		booked_hotel_rooms = select(Booking, Room).select_from(Booking).\
								join(Room, Booking.room_id == Room.id, isouter=True).\
								where(and_(Booking.date_to >= date_from),
									and_(Booking.date_from <= date_to)).cte("booked_hotel_rooms")

		get_hotels_with_remaining_rooms = select(Hotel.id,
												 Hotel.name,
												 Hotel.location,
												 Hotel.services,
												 Hotel.room_quantity,
												 Hotel.image_id,
												 ((Hotel.room_quantity - func.count(booked_hotel_rooms.c.hotel_id)).label("rooms_left"))
												 ).select_from(Hotel).join(
												booked_hotel_rooms, Hotel.id == booked_hotel_rooms.c.hotel_id, isouter=True
												).filter(cls.model.location.like(f'%{location}%')
												).having((Hotel.room_quantity - func.count(booked_hotel_rooms.c.hotel_id)) > 0
												).group_by(Hotel.id, Hotel.name, Hotel.location, Hotel.room_quantity, booked_hotel_rooms.c.hotel_id)

		async with async_session_maker() as session:
			result = await session.execute(get_hotels_with_remaining_rooms)
			return result.all()

