import codecs
import csv

from fastapi import APIRouter, File, UploadFile
from sqlalchemy import insert
from starlette.background import BackgroundTasks

from app.database import Base, async_session_maker

router = APIRouter(
	prefix="/importer",
	tags=["Добавление отелей"]
)


async def get_dict_from_csv_file(file: UploadFile, background_tasks: BackgroundTasks,):
	csv_reader = csv.DictReader(codecs.iterdecode(file.file, encoding='utf-8'))
	background_tasks.add_task(file.file.close)
	result = []
	for csv_object in list(csv_reader):
		for key in csv_object:
			try:
				csv_object[key] = int(csv_object[key])
			except:
				continue
		result.append(csv_object)
	return result


async def get_model_by_tablename(table_name: str):
	for model in Base.__subclasses__():
		if hasattr(model, '__tablename__') and model.__tablename__ == table_name:
			return model


@router.post("/upload")
async def upload(table_name: str, background_tasks: BackgroundTasks, file: UploadFile = File(...)):
	list_with_dicts_from_csv = await get_dict_from_csv_file(file, background_tasks)
	table = await get_model_by_tablename(table_name)

	for dict_element in list_with_dicts_from_csv:
		async with async_session_maker() as session:
			query = insert(table).values(**dict_element)
			await session.execute(query)
			await session.commit()

	return None



