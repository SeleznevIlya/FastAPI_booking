from app.database import Base
from sqlalchemy import Column, String, Integer, JSON, ForeignKey
from sqlalchemy.orm import relationship
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
	