from sqlalchemy.orm import relationship

from app.database import Base
from sqlalchemy import Column, String, Integer


class User(Base):
	__tablename__ = 'user'

	id = Column(Integer, primary_key=True)
	email = Column(String, nullable=False)
	hashed_password = Column(String, nullable=False)

	booking = relationship("Booking", back_populates="user")
