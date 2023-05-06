import os
import tempfile
import zipfile

from config import TEST_ZIP_NAME
from models.app import Application


def create_dummy_apps(num):
    return [Application.get_dummy_object(developer_id=i, app_name=i).save() for i in range(num)]


def create_test_zip(files):
    temp_dir = tempfile.mkdtemp()
    zip_path = os.path.join(temp_dir, TEST_ZIP_NAME)

    with zipfile.ZipFile(zip_path, 'w') as zf:
        for filename, content in files.items():
            zf.writestr(filename, content)

    return zip_path, TEST_ZIP_NAME


def remove_file(file_path):
    os.remove(file_path)


def create_corrupted_zip(file_list):
    temp_dir = tempfile.mkdtemp()
    original_zip_path, zip_name = create_test_zip(file_list)
    corrupted_zip_path = os.path.join(temp_dir, TEST_ZIP_NAME)

    with open(original_zip_path, 'rb') as original_zip, open(corrupted_zip_path, 'wb') as corrupted_zip:
        original_zip_data = original_zip.read()
        corrupted_zip.write(
            original_zip_data[:-4])  # Remove a few bytes from the original zip file to create a corrupted zip

    os.remove(original_zip_path)
    return corrupted_zip_path, TEST_ZIP_NAME
