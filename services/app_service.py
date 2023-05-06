from api.exceptions import ValidationError, NotFound
from database import db_session
from models.app import Application, AppStatus
from utils import build_query_filter


def get_app_by_id(app_id):
    app = Application.get_by_id(app_id)
    if not app:
        raise NotFound(f"Application with ID {app_id} not found.")
    return app


def get_apps(**request_args):
    query = db_session.query(Application)
    return {"apps": build_query_filter(query, request_args, Application).all()}


def create_app(developer_id, app_name):
    app = db_session.query(Application).filter(Application.developer_id == developer_id,
                                               Application.app_name == app_name).first()

    if app:
        raise ValidationError(f"Application with developer ID {developer_id} and name {app_name} already exists.")

    app = Application(developer_id=developer_id,
                      app_name=app_name,
                      app_status=AppStatus.NOT_UPLOADED.value)
    app.save()
    return app


def delete_app(app_id):
    app = get_app_by_id(app_id)
    db_session.delete(app)


def update_app_status(app_id, app_status):
    app = get_app_by_id(app_id)
    if app_status not in AppStatus.app_status_values():
        raise ValidationError(f"Invalid app status: {app_status}.")

    app.app_status = app_status
    app.save()
