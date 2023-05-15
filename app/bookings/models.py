from sqlalchemy.orm import relationship

from app.database import Base
from sqlalchemy import Column, String, Integer, JSON, ForeignKey, Date, Computed
from app.hotels.rooms.models import Room
from app.auth.models import User


class Booking(Base):
	__tablename__ = "booking"

	id = Column(Integer, primary_key=True)
	room_id = Column(Integer, ForeignKey("room.id"))
	user_id = Column(Integer, ForeignKey("user.id"))
	date_from = Column(Date, nullable=False)
	date_to = Column(Date, nullable=False)
	price = Column(Integer, nullable=False)
	total_cost = Column(Integer, Computed("(date_to - date_from)*price"))
	total_days = Column(Integer, Computed("(date_to - date_from)"))

	room = relationship('Room', back_populates='booking')
	user = relationship('User', back_populates='booking')

	def __str__(self):
		return f"Бронь №{self.id}"
