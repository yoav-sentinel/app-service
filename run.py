import multiprocessing
import signal
import sys

from waitress import serve

from database import Base, db_engine
from flask_app import flask_app
from workers import celery_worker


def run_postgres():
    Base.metadata.create_all(bind=db_engine)


def run_flask():
    serve(flask_app, host='0.0.0.0', port=5000)


def run_celery():
    celery_worker()


if __name__ == '__main__':
    # Start Celery worker in background
    celery_proc = multiprocessing.Process(target=run_celery)
    celery_proc.start()

    # Start Flask server in foreground
    flask_proc = multiprocessing.Process(target=run_flask)
    flask_proc.start()


    def signal_handler(sig, frame):
        celery_proc.terminate()
        flask_proc.terminate()
        sys.exit(0)


    signal.signal(signal.SIGINT, signal_handler)

    # Wait for Celery and Flask to finish
    celery_proc.join()
    flask_proc.join()
