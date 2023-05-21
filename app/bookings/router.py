from fastapi import APIRouter, Depends, status, Query
from pydantic import parse_obj_as

from app.auth.dependencies import get_current_user
from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBooking
from app.auth.models import User
from datetime import date, datetime

from app.exceptions import RoomCannotBeBooked
from app.tasks.tasks import send_booking_confirmation_email

router = APIRouter(
	prefix='/booking',
	tags=["Бронирование"]
)


@router.get("/")
async def get_bookings(user: User = Depends(get_current_user)) -> list[SBooking]:
	return await BookingDAO.find_all(user_id=user.id)


@router.get("/{booking_id}/", response_model=SBooking)
async def get_booking(booking_id, user: User = Depends(get_current_user)):
	pass


@router.delete("/{booking_id}/")
async def delete_booking(booking_id: int, user: User = Depends(get_current_user)):
	return await BookingDAO.delete(id=booking_id, user_id=user.id)


@router.post("/")
async def add_booking(room_id: int,
					date_from: date = Query(..., description=f"Haпpuмep, {datetime.now().date()}"),
					date_to: date = Query(..., description=f"Haпpuмep, {datetime.now().date()}"),
					user: User = Depends(get_current_user)):
	booking = await BookingDAO.add(user.id, room_id, date_from, date_to)
	if booking:
		booking_dict = parse_obj_as(SBooking, booking).dict()
		send_booking_confirmation_email.delay(booking_dict, user.email)
	else:
		raise RoomCannotBeBooked(status_code=status.HTTP_409_CONFLICT, detail="Свободных номеров нет",)
