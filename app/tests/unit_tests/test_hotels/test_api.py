import pytest
from httpx import AsyncClient


@pytest.mark.parametrize("hotel_id,date_from,date_to,status_code",[
	(1, "2023-05-21", "2023-05-22", 200),
	(1, "2023-05-21", "2023-07-22", 400),
	(1, "2023-05-21", "2023-05-20", 400),
])
async def test_get_hotels_rooms(hotel_id, date_from, date_to, status_code, authenticated_ac: AsyncClient):
	response = await authenticated_ac.get(f"/hotels/{hotel_id}/rooms", params={
		"hotel_id": hotel_id,
		"date_from": date_from,
		"date_to": date_to
	})

	assert response.status_code == status_code
