import services.app_service as app_service
from api.exceptions import ValidationError, NotFound
from database import db_session
from models.app import Application, AppStatus
from tests.tests_base import BaseTestCase


class TestAppsService(BaseTestCase):
    pass


class TestGetAppById(TestAppsService):
    def test_get_app_by_id_sanity(self):
        app = Application.get_dummy_object()
        app.save()
        app_response = app_service.get_app_by_id(app.id)
        self.assertEqual(app_response, app)

    def test_get_app_by_id_not_found(self):
        with self.assertRaises(NotFound):
            app = Application.get_dummy_object()
            app.save()
            app_service.get_app_by_id(111)

    def test_get_app_by_id_multiple_apps(self):
        expected_app = Application.get_dummy_object()
        expected_app.save()
        for i in range(10):
            Application.get_dummy_object(developer_id=i).save()
        app_response = app_service.get_app_by_id(expected_app.id)
        self.assertEqual(app_response, expected_app)


class TestGetApps(TestAppsService):
    def test_get_apps_sanity(self):
        Application.get_dummy_object(developer_id=123).save()
        Application.get_dummy_object(developer_id=456).save()
        Application.get_dummy_object(developer_id=789).save()

        apps_response = app_service.get_apps()
        self.assertEqual(len(apps_response["apps"]), 3)

    def test_get_apps_filters_developer_id(self):
        app_1 = Application.get_dummy_object(developer_id=123, app_name='abc').save()
        app_2 = Application.get_dummy_object(developer_id=123, app_name='def').save()
        Application.get_dummy_object(developer_id=456).save()

        apps_response = app_service.get_apps(developer_id=123)["apps"]
        self.assertEqual(len(apps_response), 2)
        self.assertTrue(app_1 in apps_response)
        self.assertTrue(app_2 in apps_response)

    def test_get_apps_filters_app_name(self):
        app_1 = Application.get_dummy_object(developer_id=123, app_name='abc').save()
        app_2 = Application.get_dummy_object(developer_id=456, app_name='abc').save()
        Application.get_dummy_object(developer_id=123, app_name='def').save()

        apps_response = app_service.get_apps(app_name='abc')["apps"]
        self.assertEqual(len(apps_response), 2)
        self.assertTrue(app_1 in apps_response)
        self.assertTrue(app_2 in apps_response)

    def test_get_apps_filters_app_status(self):
        app_1 = Application.get_dummy_object(developer_id=123, app_name='abc',
                                             app_status=AppStatus.APPROVED.value).save()
        app_2 = Application.get_dummy_object(developer_id=456, app_name='def',
                                             app_status=AppStatus.APPROVED.value).save()
        app_3 = Application.get_dummy_object(developer_id=789, app_name='ghi',
                                             app_status=AppStatus.DELETED.value).save()

        apps_response = app_service.get_apps(app_status=AppStatus.APPROVED.value)["apps"]
        self.assertEqual(len(apps_response), 2)
        self.assertTrue(app_1 in apps_response)
        self.assertTrue(app_2 in apps_response)

        apps_response = app_service.get_apps(app_status=AppStatus.DELETED.value)["apps"]
        self.assertEqual(len(apps_response), 1)
        self.assertTrue(app_3 in apps_response)

    def test_get_apps_filters_combinations(self):
        app_1 = Application.get_dummy_object(developer_id=123, app_name='abc',
                                             app_status=AppStatus.APPROVED.value).save()
        app_2 = Application.get_dummy_object(developer_id=456, app_name='def',
                                             app_status=AppStatus.APPROVED.value).save()

        apps_response = app_service.get_apps(app_status=AppStatus.APPROVED.value)["apps"]
        self.assertEqual(len(apps_response), 2)
        self.assertTrue(app_1 in apps_response)
        self.assertTrue(app_2 in apps_response)

        apps_response = app_service.get_apps(app_status=AppStatus.APPROVED.value, developer_id=123)["apps"]
        self.assertEqual(len(apps_response), 1)
        self.assertTrue(app_1 in apps_response)

        apps_response = app_service.get_apps(app_status=AppStatus.APPROVED.value, app_name="dummy_name")["apps"]
        self.assertEqual(len(apps_response), 0)


class TestCreateApps(TestAppsService):
    def test_create_app_sanity(self):
        app = app_service.create_app(developer_id=123, app_name='abc')
        result = db_session.query(Application).first()
        assert app == result
        assert app.app_status == AppStatus.NOT_UPLOADED.value

    def test_create_app_existing_developer_id_and_app_name(self):
        Application.get_dummy_object(developer_id=123, app_name='abc').save()
        with self.assertRaises(ValidationError):
            app_service.create_app(developer_id=123, app_name='abc')


class TestDeleteApps(TestAppsService):
    def test_delete_app_sanity(self):
        app = Application.get_dummy_object().save()
        self.assertEqual(len(db_session.query(Application).all()), 1)

        app_service.delete_app(app.id)
        db_session.commit()
        self.assertIsNone(db_session.query(Application).one_or_none())

    def test_delete_app_not_found(self):
        with self.assertRaises(NotFound):
            app_service.delete_app(123)
