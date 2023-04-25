from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.hotels.models import Hotel
from sqlalchemy import select
from datetime import date


class HotelDAO(BaseDAO):
	model = Hotel

	@classmethod
	async def find_all_by_location(cls, location:str, date_from: date,
				date_to: date):

		"""
		select * from hotels as h
		left join
		where
		"""

		async with async_session_maker() as session:
			query = select(cls.model).filter(cls.model.location.like(f'%{location}%'))
			result = await session.execute(query)
			return result.scalars().all()

