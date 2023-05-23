from datetime import timedelta

from pydantic import BaseModel, json


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

