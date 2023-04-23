from fastapi import APIRouter, Depends, status

from app.auth.dependencies import get_current_user
from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBooking
from app.auth.models import User
from datetime import date

from app.exceptions import RoomCannotBeBooked

router = APIRouter(
	prefix='/booking',
	tags=["Бронирование"]
)


@router.get("/")
async def get_bookings(user: User = Depends(get_current_user)) -> list[SBooking]:
	return await BookingDAO.find_all(user_id=user.id)


@router.get("/{booking_id}")
def get_booking(booking_id):
	pass


@router.post("/")
async def add_booking(room_id: int, date_from: date, date_to: date, user: User = Depends(get_current_user)):
	booking = await BookingDAO.add(user.id, room_id, date_from, date_to)
	if not booking:
		raise RoomCannotBeBooked(status_code=status.HTTP_409_CONFLICT, detail="Свободных номеров нет",)
