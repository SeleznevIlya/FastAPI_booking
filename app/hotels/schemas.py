
from pydantic import BaseModel, json, Field
from typing import Optional


class SHotel(BaseModel):
	id: int
	name: str
	location: str
	services: list
	room_quantity: int
	image_id: int
	rooms_left: Optional[int] = Field()

	class Config:
		orm_mode = True
