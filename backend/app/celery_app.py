from celery import Celery
from app.config import settings

celery_app = Celery(
    "worker",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)

# Optional: Configuration overrides
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

# Auto-discover tasks in submodules
celery_app.autodiscover_tasks(["app.ml", "app.services", "app.api.v1"])

@celery_app.task(name="test_celery")
def test_celery():
    return "Celery is up and running!"
