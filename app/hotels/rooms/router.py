from app.hotels.router import router


@router.get('/{hotel_id}/rooms')
async def get_hotels_rooms(hotel_id: int):
	pass
