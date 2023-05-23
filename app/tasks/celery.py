from celery import Celery

from app.config import settings

celery = Celery(
	"tasks",
	broker=f"redis://localhost:6379",
	include=["app.tasks.tasks"]
)