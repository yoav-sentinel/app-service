import os
import shutil

from config import UPLOAD_FOLDER
from services import app_service


def upload_file(app_id, file_obj, file_name):
    """
    Uploads a file to the storage for a given application.
    :param app_id: The ID of the application.
    :param file_obj: The file object.
    :param file_name: The name of the file.
    """
    app_service.get_app_by_id(app_id)
    app_upload_path = _create_app_folder(app_id)

    file_obj.seek(0)
    file_path = os.path.join(app_upload_path, file_name)
    with open(file_path, 'wb') as f:
        f.write(file_obj.read())


def _create_app_folder(app_id):
    """
    Creates a folder for the application with the given app_id.
    :param app_id: The ID of the application.
    :return: The path to the created folder.
    """
    app_upload_path = os.path.join(UPLOAD_FOLDER, str(app_id))
    os.makedirs(app_upload_path, exist_ok=True)
    return app_upload_path


def delete_app_files(app_id):
    """
    Deletes all files associated with a given application.
    :param app_id: The ID of the application.
    """
    app_upload_path = os.path.join(UPLOAD_FOLDER, str(app_id))
    shutil.rmtree(app_upload_path, ignore_errors=True)
