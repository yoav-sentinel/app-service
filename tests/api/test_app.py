import os

from config import UPLOAD_FOLDER
from models.app import Application, AppStatus
from tests.helpers import create_dummy_apps
from tests.test_base import BaseTestCase


class TestAppsAPI(BaseTestCase):
    pass


class TestCreateApp(TestAppsAPI):
    def _post_create_app(self, payload):
        return self.client.post(
            '/app',
            json=payload
        )

    def test_create_app_sanity(self):
        payload = {"developer_id": 123, "app_name": "my_app"}
        response = self._post_create_app(payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["app_name"], payload["app_name"])
        self.assertEqual(response.json["developer_id"], payload["developer_id"])

    def test_create_app_no_payload(self):
        response = self._post_create_app(payload={})
        self.assertEqual(response.status_code, 400)
        self.assertIn("app_name", response.json["error"])
        self.assertIn("developer_id", response.json["error"])

    def test_create_app_missing_app_name(self):
        payload = {"developer_id": 123}
        response = self._post_create_app(payload=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("app_name", response.json["error"])

    def test_create_app_missing_developer_id(self):
        payload = {"app_name": "my_app"}
        response = self._post_create_app(payload=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("developer_id", response.json["error"])


class TestGetAppById(TestAppsAPI):
    def _get_get_app_by_id(self, app_id=None):
        return self.client.get(
            f'/app/{app_id}',
        )

    def test_get_app_by_id_sanity(self):
        app = Application.get_dummy_object().save()

        response = self._get_get_app_by_id(app.id)

        self.inner_session.add(app)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["app_id"], app.id)
        self.assertEqual(response.json["developer_id"], app.developer_id)
        self.assertEqual(response.json["app_name"], app.app_name)

    def test_get_app_by_id_not_found(self):
        response = self._get_get_app_by_id(123)
        self.assertEqual(response.status_code, 404)
        self.assertIn("Application with ID 123 not found", response.json["error"])

    def test_get_app_by_id_multiple_apps(self):
        apps = create_dummy_apps(3)

        response = self._get_get_app_by_id(apps[2].id)

        self.inner_session.add(apps[2])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["app_id"], apps[2].id)
        self.assertEqual(response.json["developer_id"], apps[2].developer_id)
        self.assertEqual(response.json["app_name"], apps[2].app_name)


class TestGetApps(TestAppsAPI):
    def _get_get_apps(self, request_args=None):
        return self.client.get(
            '/app',
            query_string=request_args
        )

    def test_get_apps_sanity(self):
        apps = create_dummy_apps(10)
        response = self._get_get_apps()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["apps"]), 10)

        for i in range(10):
            self.inner_session.add(apps[i])
            self.assertEqual(response.json["apps"][i]["app_id"], apps[i].id)
            self.assertEqual(response.json["apps"][i]["developer_id"], apps[i].developer_id)
            self.assertEqual(response.json["apps"][i]["app_name"], apps[i].app_name)

    def test_get_apps_filter_developer_id(self):
        apps = create_dummy_apps(3)

        request_args = {"developer_id": apps[0].developer_id}
        response = self._get_get_apps(request_args)
        self.inner_session.add_all(apps)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["apps"]), 1)
        self.assertEqual(response.json["apps"][0]["app_id"], apps[0].id)
        self.assertEqual(response.json["apps"][0]["developer_id"], apps[0].developer_id)
        self.assertEqual(response.json["apps"][0]["app_name"], apps[0].app_name)

    def test_get_apps_filter_app_name(self):
        apps = create_dummy_apps(3)

        request_args = {"app_name": apps[0].app_name}
        response = self._get_get_apps(request_args)

        self.inner_session.add_all(apps)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["apps"]), 1)
        self.assertEqual(response.json["apps"][0]["app_id"], apps[0].id)
        self.assertEqual(response.json["apps"][0]["developer_id"], apps[0].developer_id)
        self.assertEqual(response.json["apps"][0]["app_name"], apps[0].app_name)

    def test_get_apps_filter_app_status(self):
        app_1 = Application.get_dummy_object(developer_id=1, app_name='abc', app_status=AppStatus.APPROVED.value).save()
        app_2 = Application.get_dummy_object(developer_id=1, app_name='def', app_status=AppStatus.APPROVED.value).save()
        _ = Application.get_dummy_object(developer_id=2, app_name='def', app_status=AppStatus.REJECTED.value).save()
        expected_apps = [app_1, app_2]

        request_args = {"app_status": AppStatus.APPROVED.value}
        response = self._get_get_apps(request_args)

        self.inner_session.add_all(expected_apps)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["apps"]), 2)

        for i in range(2):
            self.assertEqual(response.json["apps"][i]["app_id"], expected_apps[i].id)
            self.assertEqual(response.json["apps"][i]["developer_id"], expected_apps[i].developer_id)
            self.assertEqual(response.json["apps"][i]["app_name"], expected_apps[i].app_name)

    def test_get_apps_filter_app_status_invalid_status(self):
        request_args = {"app_status": "dummy_status"}
        response = self._get_get_apps(request_args)
        self.assertEqual(response.status_code, 400)
        self.assertIn("app_status", response.json["error"])
        self.assertIn("Must be one of", response.json["error"]["app_status"][0])

    def test_get_apps_filters_combination(self):
        app_1 = Application.get_dummy_object(developer_id=1, app_name='abc').save()
        app_2 = Application.get_dummy_object(developer_id=1, app_name='def').save()
        app_3 = Application.get_dummy_object(developer_id=2, app_name='def').save()

        request_args = {"developer_id": 1, "app_name": "def"}
        response = self._get_get_apps(request_args)
        self.inner_session.add_all([app_1, app_2, app_3])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["apps"]), 1)
        self.assertEqual(response.json["apps"][0]["app_id"], app_2.id)
        self.assertEqual(response.json["apps"][0]["developer_id"], app_2.developer_id)
        self.assertEqual(response.json["apps"][0]["app_name"], app_2.app_name)

    def test_get_apps_filters_multiple_matches(self):
        _ = Application.get_dummy_object(developer_id=1, app_name='abc').save()
        app_2 = Application.get_dummy_object(developer_id=1, app_name='def').save()
        app_3 = Application.get_dummy_object(developer_id=2, app_name='def').save()
        expected_apps = [app_2, app_3]

        request_args = {"app_name": "def"}
        response = self._get_get_apps(request_args)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["apps"]), 2)
        self.inner_session.add_all(expected_apps)

        for i in range(2):
            self.assertEqual(response.json["apps"][i]["app_id"], expected_apps[i].id)
            self.assertEqual(response.json["apps"][i]["developer_id"], expected_apps[i].developer_id)
            self.assertEqual(response.json["apps"][i]["app_name"], expected_apps[i].app_name)


class TestDeleteAPI(TestAppsAPI):
    def _delete_delete_apps(self, app_id=None):
        return self.client.delete(
            f'/app/{app_id}',
        )

    def test_delete_app_sanity(self):
        app = Application.get_dummy_object().save()
        app_files_path = os.path.join(UPLOAD_FOLDER, str(app.id))
        os.makedirs(app_files_path)

        response = self._delete_delete_apps(app.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["result"], f"Application {app.id} deletion successful.")
        self.assertFalse(os.path.exists(app_files_path))

    def test_delete_app_not_found(self):
        response = self._delete_delete_apps(123)
        self.assertEqual(response.status_code, 404)
        self.assertIn("Application with ID 123 not found", response.json["error"])

    def test_delete_app_with_no_files(self):
        app = Application.get_dummy_object().save()
        app_files_path = os.path.join(UPLOAD_FOLDER, str(app.id))

        response = self._delete_delete_apps(app.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["result"], f"Application {app.id} deletion successful.")
        self.assertFalse(os.path.exists(app_files_path))
