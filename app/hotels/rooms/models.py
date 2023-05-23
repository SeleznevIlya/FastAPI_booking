from sqlalchemy import JSON, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base
from app.hotels.models import Hotel


class Room(Base):
	__tablename__ = 'room'

	id = Column(Integer, primary_key=True)
	hotel_id = Column(Integer, ForeignKey('hotel.id'), nullable=False)
	name = Column(String, nullable=False)
	description = Column(String, nullable=True)
	price = Column(Integer, nullable=False)
	services = Column(JSON, nullable=True)
	quantity = Column(Integer, nullable=False)
	image_id = Column(Integer)

	hotel = relationship('Hotel', back_populates='room')
	booking = relationship('Booking', back_populates='room')

	def __str__(self):
		return f"Комната {self.name}"
