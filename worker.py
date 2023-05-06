from celery.__main__ import main as celery_main


def worker():
    celery_main(['worker', '-A', 'celery_app', '--loglevel=info', '--concurrency=4'])
