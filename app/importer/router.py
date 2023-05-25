from fastapi import APIRouter, UploadFile, File
import csv
import codecs

from starlette.background import BackgroundTasks

router = APIRouter(
	prefix="/importer",
	tags=["Добавление отелей"]
)


@router.post("/upload")
def upload(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
	csvReader = csv.DictReader(codecs.iterdecode(file.file, 'utf-8'))
	background_tasks.add_task(file.file.close)
	return list(csvReader)


