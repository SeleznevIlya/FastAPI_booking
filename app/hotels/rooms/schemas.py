from pydantic import BaseModel, json
from datetime import timedelta


class SRoom(BaseModel):
	id: int
	hotel_id: int
	name: str
	description: str | None = None
	price: int
	services: list
	quantity: int
	image_id: int

	class Config:
		orm_mode = True


class SRoomPrice(SRoom):
	total_price: int
	rooms_left: int

