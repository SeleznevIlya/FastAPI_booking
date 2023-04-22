from fastapi import APIRouter, Depends

from app.auth.dependencies import get_current_user
from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBooking
from app.auth.models import User

router = APIRouter(
	 prefix='/booking',
	tags=["Бронирование"]
)


@router.get("/")
async def get_bookings(user: User = Depends(get_current_user))  -> list[SBooking]:
	return await BookingDAO.find_all(user_id=user.id)


@router.get("/{booking_id}")
def get_booking(booking_id):
	pass
