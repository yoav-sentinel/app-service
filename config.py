import logging
import os
from enum import Enum

# project root directory
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# file upload
UPLOAD_FOLDER = os.path.join(ROOT_DIR, 'uploads')
FILE_CONTENT_EXTENSION = '.doesntmakesense'
ZIP_MIMETYPE = 'application/zip'

# postgres
DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://admin:admin@localhost:5432/apps')

# celery
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

# flask
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

# logs
LOGS_FOLDER = os.path.join(ROOT_DIR, 'logs')

# tests
TEST_ZIP_NAME = 'test.zip'


class LogLevel(Enum):
    Error = "error"
    Warn = "warn"
    Info = "info"
    Debug = "debug"


def configure_logging(app_name):
    # Create the logs directory if it doesn't exist
    os.makedirs(LOGS_FOLDER, exist_ok=True)

    # Set the log file path to logs/<app_name>.log
    log_file = os.path.join(LOGS_FOLDER, f'{app_name}.log')

    # Create the logger instance
    logger = logging.getLogger(app_name)
    logger.setLevel(logging.DEBUG)

    # Create the file handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)

    # Create the formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Add the file handler to the logger
    logger.addHandler(file_handler)

    return logger
