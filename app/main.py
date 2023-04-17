from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import Optional
from datetime import date


app = FastAPI()


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
