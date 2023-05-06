import base64

from flask import Blueprint, request
from werkzeug.utils import secure_filename

from api.decorators import api_endpoint
from api.exceptions import ValidationError
from api.schemas.app_schema import (
    AppIdPathSchema, PostAppSchema, AppResponseSchema, AppsResponseSchema,
    AppsFilterSchema, UploadAppFileResponseSchema, DeleteAppResponseSchema
)
from models.app import AppStatus
from services import app_service, storage_service
from tasks.celery_tasks import async_upload_file_task

# Define the app blueprint with the URL prefix '/app'
app_bp = Blueprint('app', __name__, url_prefix='/app')


@app_bp.route('/<int:app_id>', methods=['GET'])
@api_endpoint(url='/<int:app_id>', methods=['GET'], path_schema=AppIdPathSchema, response_schema=AppResponseSchema)
def get_app_by_id(app_id):
    """
    Endpoint to get an app by its ID.
    :param app_id: The ID of the app.
    :return: The app object with the given ID.
    """
    return app_service.get_app_by_id(app_id)


@app_bp.route('', methods=['GET'])
@api_endpoint(url='', methods=['GET'], query_schema=AppsFilterSchema, response_schema=AppsResponseSchema)
def get_apps():
    """
    Endpoint to get all apps with optional filters.
    :return: A list of apps.
    """
    return app_service.get_apps(**request.args)


@app_bp.route('', methods=['POST'])
@api_endpoint(url='', methods=['POST'], payload_schema=PostAppSchema, response_schema=AppResponseSchema)
def create_app():
    """
    Endpoint to create a new app.
    :return: The created app object.
    """
    return app_service.create_app(**request.get_json())


@app_bp.route('/<int:app_id>', methods=['DELETE'])
@api_endpoint(url='/<int:app_id>', methods=['DELETE'], path_schema=AppIdPathSchema,
              response_schema=DeleteAppResponseSchema)
def delete_app(app_id):
    """
    Endpoint to delete an app by its ID.
    :param app_id: The ID of the app.
    :return: A confirmation message for the deletion.
    """
    app_service.delete_app(app_id)
    storage_service.delete_app_files(app_id)
    return {"result": f"Application {app_id} deletion successful."}


@app_bp.route('/<int:app_id>/upload', methods=['POST'])
@api_endpoint(url='/<int:app_id>/upload', methods=['POST'], path_schema=AppIdPathSchema,
              response_schema=UploadAppFileResponseSchema)
def upload_file(app_id):
    """
    Endpoint to upload a file for an app.
    :param app_id: The ID of the app.
    :return: A confirmation message for the upload and the task ID for tracking the validation process.
    """
    app_service.get_app_by_id(app_id)

    if 'file' not in request.files:
        raise ValidationError(f"No file provided")

    app_service.update_app_status(app_id, AppStatus.UNDER_REVIEW.value)
    file = request.files['file']
    filename = secure_filename(file.filename)

    file_content = file.read()
    base64_file_content = base64.b64encode(file_content).decode()
    task = async_upload_file_task.apply_async(args=[app_id, base64_file_content, filename])

    return {
        "result": "File upload successful. Validation in progress.",
        "task_id": task.id}
