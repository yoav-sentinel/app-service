from celery import Celery
from celery.utils.log import get_task_logger

from config import CELERY_RESULT_BACKEND, CELERY_BROKER_URL, configure_logging

logger = configure_logging('celery')

celery = Celery(backend=CELERY_RESULT_BACKEND, broker=CELERY_BROKER_URL)

celery.conf.update(
    {
        "CELERY_IMPORTS": (
            "tasks.celery_tasks",
        ),
    }
)

# Set the Celery logger to use the logging module
celery_log = get_task_logger(__name__)
celery_log.propagate = False
celery_log.handlers = logger.handlers
