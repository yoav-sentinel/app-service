import base64
import logging
from io import BytesIO

from celery_app import celery
from database import db_session
from models.app import AppStatus, Application
from services import review_service, storage_service, app_service

logger = logging.getLogger('celery')


@celery.task()
def async_upload_file_task(app_id, base64_file_content, file_name):
    file_content = base64.b64decode(base64_file_content)
    file_obj = BytesIO(file_content)

    try:
        logger.info("Starting uploaded file validations")
        review_service.validate_uploaded_file(file_obj, file_name)
        logger.info("Uploaded file validations success")

        logger.info("Uploading file")
        storage_service.upload_file(app_id, file_obj, file_name)
        logger.info("Uploading file success")

        logger.info("Updating app status to Approved")
        app_service.update_app_status(app_id, AppStatus.APPROVED.value)

        db_session.commit()

    except ValueError as e:
        logger.info(f"Uploaded file validations failure: {str(e)}")
        logger.info("Updating app status to Rejected")
        app_service.update_app_status(app_id, AppStatus.REJECTED.value)
        db_session.commit()
        return

    except Exception as e:
        logger.info(f"Upload file unexpected error: {str(e)}")
        app_service.update_app_status(app_id, AppStatus.REJECTED.value)
        db_session.commit()
        return
