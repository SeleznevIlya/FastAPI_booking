import pytest
from httpx import AsyncClient


@pytest.mark.parametrize("room_id,date_from,date_to,status_code", [
	*[(4, '2023-05-27', '2023-05-29', 200)]*8,
	(4, '2023-05-27', '2023-05-29', 409),
	(4, '2023-05-27', '2023-05-29', 409)
])
async def test_add_and_get_booking(room_id, date_from, date_to, status_code,
								authenticated_ac: AsyncClient):
	response = await authenticated_ac.post("/booking/", params={
		"room_id": room_id,
		"date_from": date_from,
		"date_to": date_to
	})

	assert response.status_code == status_code


async def test_get_and_delete_booking(authenticated_ac: AsyncClient):
	request = await authenticated_ac.get("/booking/")
	for booking in request.json():
		await authenticated_ac.delete(f"/booking/{booking['id']}/", params={"id": booking["id"]})
	request = await authenticated_ac.get("/booking/")

	assert len(request.json()) == 0
	