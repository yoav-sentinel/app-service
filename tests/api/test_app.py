import io
import os
import unittest
import zipfile

from celery.result import AsyncResult
from flask import json

from celery_app import celery
from config import TEST_ZIP_PATH
from flask_app import flask_app
from tests.helpers import create_test_zip, remove_file, create_corrupted_zip


class TestUploadFileAPI(unittest.TestCase):
    def setUp(self):
        self.app = flask_app
        self.celery = celery
        self.client = self.app.test_client()

    def upload_and_validate_files_not_saved(self, file_name, file_content):
        response = self.client.post(
            '/app/upload?appId=123',
            content_type='multipart/form-data',
            data={'file': (
                io.BytesIO(file_content.encode() if isinstance(file_content, str) else file_content), file_name)},
        )

        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['result'], 'File upload successful. Validation in progress.')

        # Wait for the Celery task to finish
        task_id = response_data['task_id']
        task_result = AsyncResult(task_id, app=self.celery)
        task_result.get(timeout=10)
        self.assertFalse(os.path.exists(TEST_ZIP_PATH),
                         f"File {file_name} should not have been saved at {TEST_ZIP_PATH}")

    def test_upload_valid_zip_sanity(self):
        expected_files = {
            'file1.doesntmakesense': 'text1',
            'file2.doesntmakesense': 'text2',
        }

        zip_path, zip_name = create_test_zip(expected_files)

        with open(zip_path, 'rb') as f:
            response = self.client.post(
                '/app/upload?appId=123',
                content_type='multipart/form-data',
                data={'file': (io.BytesIO(f.read()), 'test.zip')},
            )

        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['result'], 'File upload successful. Validation in progress.')

        # Wait for the Celery task to finish
        task_id = response_data['task_id']
        task_result = AsyncResult(task_id, app=self.celery)
        task_result.get(timeout=10)

        # Check the content of the saved file
        for filename, expected_content in expected_files.items():
            with zipfile.ZipFile(TEST_ZIP_PATH, 'r') as zf:
                with zf.open(filename, 'r') as f:
                    content = f.read().decode()
                    self.assertEqual(content, expected_content, f"Content of {filename} is incorrect")

        remove_file(TEST_ZIP_PATH)

    def test_upload_without_appId(self):
        response = self.client.post('/app/upload', content_type='multipart/form-data')
        self.assertEqual(response.status_code, 400)

    def test_upload_without_file(self):
        response = self.client.post('/app/upload?appId=123', content_type='multipart/form-data')
        self.assertEqual(response.status_code, 400)

    def test_upload_non_zip_extension(self):
        self.upload_and_validate_files_not_saved("file.txt", "text file content")

    def test_upload_multiple_extensions(self):
        self.upload_and_validate_files_not_saved("file.zip.txt", "text file content")

    def test_upload_corrupted_zip(self):
        files_list = {
            'file1.doesntmakesense': 'text1',
            'file2.doesntmakesense': 'text2',
        }
        corrupted_zip_path, corrupted_zip_name = create_corrupted_zip(files_list)
        with open(corrupted_zip_path, 'rb') as f:
            self.upload_and_validate_files_not_saved(corrupted_zip_name, f.read())
