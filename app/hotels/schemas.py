from typing import Optional

from pydantic import BaseModel, Field, json


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

