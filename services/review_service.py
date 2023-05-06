import mimetypes
import os
import zipfile

from api.exceptions import ValidationError
from config import FILE_CONTENT_EXTENSION, ZIP_MIMETYPE

INVALID_FILE_TYPE = "Invalid file type. Only zip files are allowed."
INVALID_OR_CORRUPT_ZIP = "Invalid or corrupted zip file."
INVALID_CONTENT_EXTENSIONS = "The zip file contains files with unsupported extensions."


def _is_valid_zip_file_content(file_path):
    """
    Checks if the content of a zip file has valid file extensions.
    :param file_path: The path to the zip file.
    :return: True if all files in the zip have a valid extension, False otherwise.
    """
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        file_extensions = (os.path.splitext(file)[-1] for file in zip_ref.namelist())
        return all(ext == FILE_CONTENT_EXTENSION for ext in file_extensions)


def _is_valid_zip_file(file_path):
    """
    Checks if a file is a valid and non-corrupted zip file.
    :param file_path: The path to the file.
    :return: True if the file is a valid zip file, False otherwise.
    """
    try:
        with zipfile.ZipFile(file_path) as file:
            file.testzip()
        return True
    except zipfile.BadZipFile:
        return False


def _is_valid_mime_type(file_name):
    """
    Checks if a file has a valid MIME type.
    :param file_name: The name of the file.
    :return: True if the file has a valid MIME type, False otherwise.
    """
    file_mimetype, _ = mimetypes.guess_type(file_name)
    return file_mimetype == ZIP_MIMETYPE


def validate_uploaded_file(file_obj, file_name):
    """
    Validates an uploaded file based on its MIME type and the contents of the file.
    :param file_obj: The file object.
    :param file_name: The name of the file.
    :raises ValidationError: If the file MIME type is invalid, the file is not a valid zip file, or
                             the content has unsupported extensions.
    """
    if not _is_valid_mime_type(file_name):
        raise ValidationError(INVALID_FILE_TYPE)

    if not _is_valid_zip_file(file_obj):
        raise ValidationError(INVALID_OR_CORRUPT_ZIP)

    if not _is_valid_zip_file_content(file_obj):
        raise ValidationError(INVALID_CONTENT_EXTENSIONS)
