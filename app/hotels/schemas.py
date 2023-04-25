
from pydantic import BaseModel, json


class SHotel(BaseModel):
	id: int
	name: str
	location: str
	services: list
	room_quantity: int
	image_id: int
