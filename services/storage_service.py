import os

from config import UPLOAD_FOLDER
from services import app_service


def upload_file(app_id, file_obj, file_name):
    app_service.get_app_by_id(app_id)
    app_upload_path = _create_app_folder(app_id)

    file_obj.seek(0)
    file_path = os.path.join(app_upload_path, file_name)
    with open(file_path, 'wb') as f:
        f.write(file_obj.read())


def _create_app_folder(app_id):
    app_upload_path = os.path.join(UPLOAD_FOLDER, str(app_id))
    os.makedirs(app_upload_path, exist_ok=True)
    return app_upload_path
