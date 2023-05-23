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


@pytest.mark.parametrize("room_id,date_from,date_to,status_code", [
	(4, '2023-05-27', '2023-05-30', 200),
])
async def test_add_get_delete_get_booking(room_id, date_from, date_to, status_code,
										  authenticated_ac: AsyncClient):
	response = await authenticated_ac.post("/booking/", params={
		"room_id": room_id,
		"date_from": date_from,
		"date_to": date_to
	})
	# print(response.content)

	assert response.status_code == status_code

	request = await authenticated_ac.get(f"/booking/{12}/")
	print(request.json())

	assert request.json()["id"] == 12

	await authenticated_ac.delete(f"/booking/{request.json()['id']}/", params={"id": request.json()["id"]})

	request = await authenticated_ac.get(f"/booking/{12}/")

	assert request.json() is None


