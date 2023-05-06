from multiprocessing import Process

from waitress import serve

from database import Base, db_engine
from flask_app import flask_app
from worker import worker


def run_postgres():
    Base.metadata.create_all(bind=db_engine)


def run_flask():
    serve(flask_app, host='0.0.0.0', port=5000)


def run_celery():
    worker()


if __name__ == '__main__':
    # Initialize the PostgreSQL database and create the tables if they don't exist
    run_postgres()

    flask_process = Process(target=run_flask)
    celery_process = Process(target=run_celery)

    flask_process.start()
    celery_process.start()

    flask_process.join()
    celery_process.join()
