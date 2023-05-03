from celery_app import celery


def worker():
    celery.start(argv=['celery', 'worker', '--loglevel=info', '--concurrency=4'])
