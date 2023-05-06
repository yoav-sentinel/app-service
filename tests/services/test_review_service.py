import os
from io import BytesIO

from api.exceptions import ValidationError
from services.review_service import validate_uploaded_file, INVALID_CONTENT_EXTENSIONS, INVALID_OR_CORRUPT_ZIP, \
    INVALID_FILE_TYPE
from tests.helpers import create_test_zip, remove_file, create_corrupted_zip
from tests.tests_base import BaseTestCase


class BaseZipValidatorTest(BaseTestCase):
    def _assert_file_uploaded(self, file_path, file_content, file_name):
        self.assertIsNone(validate_uploaded_file(file_content, file_name))
        remove_file(file_path)

    def _assert_file_raised_error(self, file_path, file_content, file_name, error_message):
        with self.assertRaises(ValidationError) as cm:
            validate_uploaded_file(file_content, file_name)
        self.assertTrue(cm.exception.args[0] == error_message)
        remove_file(file_path)


class TestZipValidator(BaseZipValidatorTest):
    def test_valid_zip_file(self):
        file_list = {
            'file1.doesntmakesense': 'text1',
            'file2.doesntmakesense': 'text2',
        }
        zip_path, zip_name = create_test_zip(file_list)

        with open(zip_path, 'rb') as f:
            file_content = f.read()
        file_name = os.path.basename(zip_path)

        self._assert_file_uploaded(zip_path, BytesIO(file_content), file_name)

    def test_invalid_mime_type(self):
        file_path = 'test.txt'
        with open(file_path, 'w') as f:
            f.write('This is not a zip file.')

        with open(file_path, 'rb') as f:
            file_content = f.read()
        file_name = os.path.basename(file_path)

        self._assert_file_raised_error(file_path, BytesIO(file_content), file_name, INVALID_FILE_TYPE)

    def test_corrupted_zip_file(self):
        file_list = {
            'file1.doesntmakesense': 'text1',
            'file2.doesntmakesense': 'text2',
        }
        corrupted_zip_path, _ = create_corrupted_zip(file_list)

        with open(corrupted_zip_path, 'rb') as f:
            file_content = f.read()
        file_name = os.path.basename(corrupted_zip_path)

        self._assert_file_raised_error(corrupted_zip_path, BytesIO(file_content), file_name, INVALID_OR_CORRUPT_ZIP)


class TestZipContentValidator(BaseZipValidatorTest):
    def test_valid_zip_content_sanity(self):
        file_list = {
            'file1.doesntmakesense': 'text1',
            'file2.doesntmakesense': 'text2',
        }
        zip_path, zip_name = create_test_zip(file_list)

        with open(zip_path, 'rb') as f:
            file_content = f.read()
        file_name = os.path.basename(zip_path)

        self._assert_file_uploaded(zip_path, BytesIO(file_content), file_name)

    def test_invalid_zip_content_sanity(self):
        file_list = {
            'file1.doesntmakesense': 'text1',
            'file2.txt': 'text2',
        }
        zip_path, zip_name = create_test_zip(file_list)

        with open(zip_path, 'rb') as f:
            file_content = f.read()
        file_name = os.path.basename(zip_path)

        self._assert_file_raised_error(zip_path, BytesIO(file_content), file_name, INVALID_CONTENT_EXTENSIONS)

    def test_invalid_zip_content_multiple_extensions(self):
        file_list = {
            'file1.doesntmakesense': 'text1',
            'file2.doesntmakesense.dummy': 'text1'
        }
        zip_path, zip_name = create_test_zip(file_list)

        with open(zip_path, 'rb') as f:
            file_content = f.read()
        file_name = os.path.basename(zip_path)

        self._assert_file_raised_error(zip_path, BytesIO(file_content), file_name, INVALID_CONTENT_EXTENSIONS)
