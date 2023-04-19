from app.dao.base import BaseDAO
from app.bookings.models import Booking


class BookingDAO(BaseDAO):
	model = Booking
		
