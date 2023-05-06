import io
import os
import zipfile

from celery.result import AsyncResult
from flask import json

from config import UPLOAD_FOLDER, TEST_ZIP_NAME
from database import db_session
from models.app import Application, AppStatus
from tests.helpers import create_test_zip, remove_file, create_corrupted_zip
from tests.test_base import BaseCeleryTestCase


class TestUploadFileAPI(BaseCeleryTestCase):
    def upload_and_validate_files_not_saved(self, app_id, file_name, file_content):
        zip_path = os.path.join(UPLOAD_FOLDER, str(app_id), TEST_ZIP_NAME)

        response = self.client.post(
            f'/app/{app_id}/upload',
            content_type='multipart/form-data',
            data={'file': (
                io.BytesIO(file_content.encode() if isinstance(file_content, str) else file_content), file_name)},
        )

        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['result'], 'File upload successful. Validation in progress.')

        app = db_session.query(Application).first()
        self.assertEqual(app.app_status, AppStatus.UNDER_REVIEW.value)

        # Wait for the Celery task to finish
        task_id = response_data['task_id']
        task_result = AsyncResult(task_id, app=self.celery)
        task_result.get(timeout=10)

        self.assertFalse(os.path.exists(zip_path),
                         f"File {file_name} should not have been saved at {zip_path}")

        db_session.refresh(app)
        self.assertEqual(app.app_status, AppStatus.REJECTED.value)

    def test_upload_valid_zip_sanity(self):
        app = Application.get_dummy_object().save()
        uploaded_zip_path = os.path.join(UPLOAD_FOLDER, str(app.id), TEST_ZIP_NAME)

        expected_files = {
            'file1.doesntmakesense': 'text1',
            'file2.doesntmakesense': 'text2',
        }

        zip_path, zip_name = create_test_zip(expected_files)

        with open(zip_path, 'rb') as f:
            response = self.client.post(
                f'/app/{app.id}/upload',
                content_type='multipart/form-data',
                data={'file': (io.BytesIO(f.read()), 'test.zip')},
            )

        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)

        app = db_session.query(Application).first()
        self.assertEqual(app.app_status, AppStatus.UNDER_REVIEW.value)

        self.assertEqual(response_data['result'], 'File upload successful. Validation in progress.')

        # Wait for the Celery task to finish
        task_id = response_data['task_id']
        task_result = AsyncResult(task_id, app=self.celery)
        task_result.get(timeout=10)

        # Check the content of the saved file
        for filename, expected_content in expected_files.items():
            with zipfile.ZipFile(uploaded_zip_path, 'r') as zf:
                with zf.open(filename, 'r') as f:
                    content = f.read().decode()
                    self.assertEqual(content, expected_content, f"Content of {filename} is incorrect")

        remove_file(zip_path)

        db_session.refresh(app)
        self.assertEqual(app.app_status, AppStatus.APPROVED.value)

    def test_upload_without_app_id(self):
        response = self.client.post('/app/upload', content_type='multipart/form-data')
        self.assertEqual(response.status_code, 404)

    def test_upload_app_not_exist(self):
        app = Application.get_dummy_object().save()
        response = self.client.post(f'/app/{app.id + 1}/upload', content_type='multipart/form-data')
        self.assertEqual(response.status_code, 404)

    def test_upload_without_file(self):
        app = Application.get_dummy_object().save()
        response = self.client.post(f'/app/{app.id}/upload', content_type='multipart/form-data')
        self.assertEqual(response.status_code, 400)

    def test_upload_non_zip_extension(self):
        app = Application.get_dummy_object().save()
        self.upload_and_validate_files_not_saved(app.id, "file.txt", "text file content")

    def test_upload_multiple_extensions(self):
        app = Application.get_dummy_object().save()
        self.upload_and_validate_files_not_saved(app.id, "file.zip.txt", "text file content")

    def test_upload_corrupted_zip(self):
        app = Application.get_dummy_object().save()
        files_list = {
            'file1.doesntmakesense': 'text1',
            'file2.doesntmakesense': 'text2',
        }
        corrupted_zip_path, corrupted_zip_name = create_corrupted_zip(files_list)
        with open(corrupted_zip_path, 'rb') as f:
            self.upload_and_validate_files_not_saved(app.id, corrupted_zip_name, f.read())
