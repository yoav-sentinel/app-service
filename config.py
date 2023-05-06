import os

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
CELERY_LOGS = os.path.join(LOGS_FOLDER, 'celery.log')
FLASK_LOGS = os.path.join(LOGS_FOLDER, 'flask.log')

# tests
TEST_ZIP_NAME = 'test.zip'
