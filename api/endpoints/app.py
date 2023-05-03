import base64

from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename

from api.decorators import api_endpoint, timer
from api.schemas.app_schema import UploadAppFileQueryStringSchema
from tasks.celery_tasks import async_validate_uploaded_file

app_bp = Blueprint('app', __name__, url_prefix='/app')


@timer()
@app_bp.route('/upload', methods=['POST'])
@api_endpoint(url='/upload', methods=['POST'], query_schema=UploadAppFileQueryStringSchema())
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    filename = secure_filename(file.filename)

    file_content = file.read()
    base64_file_content = base64.b64encode(file_content).decode()
    task = async_validate_uploaded_file.apply_async(args=[base64_file_content, filename])

    return jsonify({
        "result": "File upload successful. Validation in progress.",
        "task_id": task.id})
