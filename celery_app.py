from celery import Celery
from celery.signals import task_prerun

from config import CELERY_RESULT_BACKEND, CELERY_BROKER_URL
from database import db_session

celery = Celery(backend=CELERY_RESULT_BACKEND, broker=CELERY_BROKER_URL)
celery.db_session = db_session

celery.conf.update(
    {
        "CELERY_IMPORTS": (
            "tasks.celery_tasks",
        ),
    }
)


@task_prerun.connect
def task_prerun_handler(**_kwargs):
    db_session.flush()
