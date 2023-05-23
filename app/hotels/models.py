from sqlalchemy import JSON, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Hotel(Base):
	__tablename__ = "hotel"

	id = Column(Integer, primary_key=True)
	name = Column(String, nullable=False)
	location = Column(String, nullable=False)
	services = Column(JSON, nullable=False)
	room_quantity = Column(Integer, nullable=False)
	image_id = Column(Integer)

	room = relationship('Room', back_populates="hotel")

	def __str__(self):
		return f"Отель {self.name}"