from fastapi import APIRouter, UploadFile, File
import csv
import codecs
from sqlalchemy import insert
from starlette.background import BackgroundTasks
from app.hotels.schemas import SHotel
from app.hotels.models import Hotel

from app.database import async_session_maker

router = APIRouter(
	prefix="/importer",
	tags=["Добавление отелей"]
)


@router.post("/upload")
async def upload(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
	csv_reader = csv.DictReader(codecs.iterdecode(file.file, 'utf-8'))
	background_tasks.add_task(file.file.close)
	for hotel in list(csv_reader):
		for key in hotel:
			try:
				hotel[key] = int(hotel[key])
			except:
				continue
		async with async_session_maker() as session:
			query = insert(Hotel).values(**hotel)
			await session.execute(query)
			await session.commit()
	return None



