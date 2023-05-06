import base64

from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename

from api.decorators import api_endpoint
from api.exceptions import ValidationError
from api.schemas.app_schema import AppIdPathSchema, PostAppSchema, AppResponseSchema, \
    AppsResponseSchema, AppsFilterSchema, UploadAppFileResponseSchema
from models.app import AppStatus
from services import app_service
from tasks.celery_tasks import async_upload_file_task

app_bp = Blueprint('app', __name__, url_prefix='/app')


@app_bp.route('/<int:app_id>', methods=['GET'])
@api_endpoint(url='/<int:app_id>', methods=['GET'], path_schema=AppIdPathSchema, response_schema=AppResponseSchema)
def get_app_by_id(app_id):
    return app_service.get_app_by_id(app_id)


@app_bp.route('/', methods=['GET'])
@api_endpoint(url='/', methods=['GET'], query_schema=AppsFilterSchema, response_schema=AppsResponseSchema)
def get_apps(query_input):
    return app_service.get_apps(**query_input)


@app_bp.route('/', methods=['POST'])
@api_endpoint(url='/', methods=['POST'], payload_schema=PostAppSchema, response_schema=AppsResponseSchema)
def create_app(payload):
    return app_service.create_app(**payload)


@app_bp.route('/<int:app_id>', methods=['DELETE'])
@api_endpoint(url='/<int:app_id>', methods=['DELETE'], path_schema=AppIdPathSchema)
def delete_app(app_id):
    return app_service.delete_app(app_id)


@app_bp.route('/<int:app_id>/upload', methods=['POST'])
@api_endpoint(url='/<int:app_id>/upload', methods=['POST'], path_schema=AppIdPathSchema,
              response_schema=UploadAppFileResponseSchema)
def upload_file(app_id):
    app_service.get_app_by_id(app_id)

    if 'file' not in request.files:
        raise ValidationError(f"No file provided")

    app_service.update_app_status(app_id, AppStatus.UNDER_REVIEW.value)
    file = request.files['file']
    filename = secure_filename(file.filename)

    file_content = file.read()
    base64_file_content = base64.b64encode(file_content).decode()
    task = async_upload_file_task.apply_async(args=[app_id, base64_file_content, filename])

    return jsonify({
        "result": "File upload successful. Validation in progress.",
        "task_id": task.id})
