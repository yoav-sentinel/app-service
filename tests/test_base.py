import os
import shutil
import unittest

from sqlalchemy.orm import sessionmaker

from celery_app import celery
from config import UPLOAD_FOLDER
from database import db_session as global_db_session, create_scoped_session, db_engine
from flask_app import flask_app
from models.app import Application
from tests.helpers import create_dummy_apps


class BaseTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_db_session = create_scoped_session(db_engine)

    def setUp(self):
        self.app = flask_app
        self.celery = celery
        self.client = self.app.test_client()

        self._original_db_session = global_db_session.registry()
        self.test_db_session.begin_nested()
        self.inner_session = sessionmaker(bind=self.test_db_session.connection())()
        self.use_test_db_session()

    def tearDown(self):
        self.inner_session.close()
        self.test_db_session.close()
        global_db_session.registry.set(self._original_db_session)

        shutil.rmtree(UPLOAD_FOLDER)
        os.mkdir(UPLOAD_FOLDER)

    def use_test_db_session(self):
        global_db_session.registry.set(self.inner_session)


class BaseCeleryTestCase(unittest.TestCase):
    def setUp(self):
        self.app = flask_app
        self.celery = celery
        self.client = self.app.test_client()

    def tearDown(self):
        global_db_session.query(Application).delete()
        global_db_session.commit()
        shutil.rmtree(UPLOAD_FOLDER)
        os.mkdir(UPLOAD_FOLDER)


class TestTestsConfiguration(BaseTestCase):
    def test_tests_commits(self):
        create_dummy_apps(10)
        global_db_session.commit()
        self.assertEqual(len(global_db_session.query(Application).all()), 10)

    def test_tests_rollbacks(self):
        self.assertEqual(len(global_db_session.query(Application).all()), 0)
