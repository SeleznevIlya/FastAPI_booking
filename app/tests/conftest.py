import asyncio
import json
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy import insert

from app.auth.models import User
from app.bookings.models import Booking
from app.config import settings
from app.database import Base, async_session_maker, engine
from app.hotels.models import Hotel
from app.hotels.rooms.models import Room
from app.main import app as fastapi_app


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
	assert settings.MODE == "TEST"

	async with engine.begin() as conn:
		await conn.run_sync(Base.metadata.drop_all)
		await conn.run_sync(Base.metadata.create_all)

	def open_mock_json(model: str):
		with open(f"app/tests/mock_{model}.json", encoding="utf-8") as file:
			return json.load(file)

	hotels = open_mock_json("hotels")
	rooms = open_mock_json("rooms")
	users = open_mock_json("users")
	bookings = open_mock_json("bookings")

	for booking in bookings:
		booking["date_from"] = datetime.strptime(booking["date_from"], "%Y-%m-%d",)
		booking["date_to"] = datetime.strptime(booking["date_to"], "%Y-%m-%d",)

	async with async_session_maker() as session:
		add_hotels = insert(Hotel).values(hotels)
		add_rooms = insert(Room).values(rooms)
		add_users = insert(User).values(users)
		add_bookings = insert(Booking).values(bookings)

		await session.execute(add_hotels)
		await session.execute(add_rooms)
		await session.execute(add_users)
		await session.execute(add_bookings)

		await session.commit()


@pytest.fixture(scope="session")
def event_loop(request):
	"""Create an instance of the default event loop for each test case."""
	loop = asyncio.get_event_loop_policy().new_event_loop()
	yield loop
	loop.close()


@pytest.fixture(scope="function")
async def ac():
	async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
		yield ac


@pytest.fixture(scope="session")
async def authenticated_ac():
	async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
		await ac.post("/v1/auth/login", json={
				'email': "test@test.com",
				'password': 'test'
		})
		assert ac.cookies['booking_access_token']
		yield ac


@pytest.fixture(scope="function")
async def session():
	async with async_session_maker() as session:
		yield session

