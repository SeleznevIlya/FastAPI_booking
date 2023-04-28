from pydantic import BaseModel, json
from datetime import timedelta


class SRoom(BaseModel):
	id: int
	hotel_id: int
	name: str
	description: str
	price: int
	services: list
	quantity: int
	image_id: int

	class Config:
		orm_mode = True


class SRoom_Price(BaseModel):
	id: int
	hotel_id: int
	name: str
	total_price: timedelta

	class Config:
		orm_mode = True
