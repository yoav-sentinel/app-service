import mimetypes
import os
import zipfile

from config import FILE_CONTENT_EXTENSION, ZIP_MIMETYPE

INVALID_FILE_TYPE = "Invalid file type. Only zip files are allowed."
INVALID_OR_CORRUPT_ZIP = "Invalid or corrupted zip file."
INVALID_CONTENT_EXTENSIONS = "The zip file contains files with unsupported extensions."


def _is_valid_zip_file_content(file_path):
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        file_extensions = (os.path.splitext(file)[-1] for file in zip_ref.namelist())
        return all(ext == FILE_CONTENT_EXTENSION for ext in file_extensions)


def _is_valid_zip_file(file_path):
    try:
        with zipfile.ZipFile(file_path) as file:
            file.testzip()
        return True
    except zipfile.BadZipFile:
        return False


def _is_valid_mime_type(file_name):
    file_mimetype, _ = mimetypes.guess_type(file_name)
    return file_mimetype == ZIP_MIMETYPE


def validate_uploaded_file(file_obj, file_name):
    if not _is_valid_mime_type(file_name):
        raise ValueError(INVALID_FILE_TYPE)

    if not _is_valid_zip_file(file_obj):
        raise ValueError(INVALID_OR_CORRUPT_ZIP)

    if not _is_valid_zip_file_content(file_obj):
        raise ValueError(INVALID_CONTENT_EXTENSIONS)
