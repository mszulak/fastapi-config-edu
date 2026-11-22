from celery import Celery
from sqlmodel import Session

from app.core.config import settings
from app.db.session import engine
from app.models.task import Task

celery_app = Celery("worker", broker=settings.redis_url, backend=settings.redis_url)


@celery_app.task
def run_heavy_task(task_id: int):
    with Session(engine) as session:
        task = session.get(Task, task_id)
        if task is not None:
            task.status = "completed"
            session.add(task)
            session.commit()
