import os.path
import zipfile

from api.exceptions import NotFound
from config import UPLOAD_FOLDER
from models.app import Application
from services import storage_service
from tests.helpers import create_test_zip
from tests.test_base import BaseTestCase


class TestStorageService(BaseTestCase):
    pass


class TestUploadFile(TestStorageService):
    def test_upload_file_sanity(self):
        app = Application.get_dummy_object().save()
        expected_files = {
            'file1.doesntmakesense': 'text1',
            'file2.doesntmakesense': 'text2',
        }

        zip_path, zip_name = create_test_zip(expected_files)

        with open(zip_path, 'rb') as file:
            storage_service.upload_file(app.id, file, zip_name)

        uploaded_zip_path = os.path.join(UPLOAD_FOLDER, str(app.id), zip_name)
        self.assertTrue(os.path.exists(uploaded_zip_path))

        # Check the content of the saved file
        for filename, expected_content in expected_files.items():
            with zipfile.ZipFile(uploaded_zip_path, 'r') as zf:
                with zf.open(filename, 'r') as f:
                    content = f.read().decode()
                    self.assertEqual(content, expected_content, f"Content of {filename} is incorrect")

    def test_upload_file_app_not_found(self):
        expected_files = {
            'file1.doesntmakesense': 'text1',
            'file2.doesntmakesense': 'text2',
        }

        zip_path, zip_name = create_test_zip(expected_files)

        with self.assertRaises(NotFound):
            with open(zip_path, 'rb') as file:
                storage_service.upload_file(123, file, zip_name)


class TestDeleteAppFiles(TestStorageService):
    def test_delete_app_files(self):
        app_1 = os.path.join(UPLOAD_FOLDER, "1")
        app_2 = os.path.join(UPLOAD_FOLDER, "2")
        app_3 = os.path.join(UPLOAD_FOLDER, "3")

        os.makedirs(app_1)
        os.makedirs(app_2)
        os.makedirs(app_3)

        storage_service.delete_app_files(app_1)
        self.assertFalse(os.path.exists(app_1))
        self.assertTrue(os.path.exists(app_2))
        self.assertTrue(os.path.exists(app_3))

        storage_service.delete_app_files(app_2)
        self.assertFalse(os.path.exists(app_1))
        self.assertFalse(os.path.exists(app_2))
        self.assertTrue(os.path.exists(app_3))

        storage_service.delete_app_files(app_3)
        self.assertFalse(os.path.exists(app_1))
        self.assertFalse(os.path.exists(app_2))
        self.assertFalse(os.path.exists(app_3))
