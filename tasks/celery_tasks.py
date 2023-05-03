import base64
import logging
import os
from io import BytesIO

from celery_app import celery
from config import UPLOAD_FOLDER
from services.review_service import validate_uploaded_file

logger = logging.getLogger('celery')


# @celery.task(bind=True)
# def async_validate_uploaded_file(self, base64_file_content, file_name):
#     file_content = base64.b64decode(base64_file_content)
#     file_obj = BytesIO(file_content)
#
#     logger.info("Starting uploaded file validations")
#     is_valid, message = validate_uploaded_file(file_obj, file_name)
#     if not is_valid:
#         logger.info(f"Uploaded file validations failure: {message}")
#         return
#
#     logger.info("Uploaded file validations success")
#     # Save the file to disk
#     file_obj.seek(0)  # Reset the file pointer to the beginning of the file
#     file_path = os.path.join(UPLOAD_FOLDER, file_name)
#     with open(file_path, 'wb') as f:
#         f.write(file_obj.read())
#
#     # Update the app table in your database here

@celery.task()
def async_validate_uploaded_file(base64_file_content, file_name):
    file_content = base64.b64decode(base64_file_content)
    file_obj = BytesIO(file_content)

    try:
        logger.info("Starting uploaded file validations")
        validate_uploaded_file(file_obj, file_name)

        logger.info("Uploaded file validations success")
        # Save the file to disk
        file_obj.seek(0)  # Reset the file pointer to the beginning of the file
        file_path = os.path.join(UPLOAD_FOLDER, file_name)
        with open(file_path, 'wb') as f:
            f.write(file_obj.read())

        # Update the app table in your database here

    except ValueError as e:
        logger.info(f"Uploaded file validations failure: {str(e)}")
        return
