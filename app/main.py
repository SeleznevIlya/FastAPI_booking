from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import Optional
from datetime import date

from app.bookings.router import router as router_bookings
from app.auth.router import router as auth_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(router_bookings)


class HotelsSearchArgs:
	def __init__(self,
			   locations: str,
			   date_from: date,
			   date_to: date,
			   stars: Optional[int]= None):
		self.locations = locations
		self.date_from = date_from
		self.date_to = date_to
		self.stars = stars


@app.get('/hotels/')
def get_hotels(
		search_args: HotelsSearchArgs = Depends()
):
	return search_args


class SBooking(BaseModel):
	room_id: int
	date_from: date
	date_to: date


@app.post('/booking/')
def add_booking(booking: SBooking):
	pass
