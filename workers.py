import subprocess

from config import CELERY_LOGS


def celery_worker():
    with open(CELERY_LOGS, 'w') as f:
        subprocess.run(['celery', '-A', 'celery_app', 'worker', '--loglevel=info', '--concurrency=4'], stdout=f)
