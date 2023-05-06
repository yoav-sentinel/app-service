import http
import logging
from logging.handlers import RotatingFileHandler

from flask import Flask, jsonify
from sqlalchemy.exc import SQLAlchemyError

from api.endpoints.app import app_bp
from api.exceptions import ERROR_STATUS_CODES
from config import UPLOAD_FOLDER, MAX_CONTENT_LENGTH, FLASK_LOGS
from database import db_session


def create_flask_app():
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
    app.debug = True

    app.register_blueprint(app_bp)
    return app


flask_app = create_flask_app()

# Set up logging
handler = RotatingFileHandler(FLASK_LOGS, maxBytes=10000, backupCount=1)
handler.setLevel(logging.INFO)
flask_app.logger.addHandler(handler)


@flask_app.before_request
def begin_nested_transaction():
    db_session.begin_nested()


@flask_app.after_request
def session_commit(response):
    if response.status_code >= http.HTTPStatus.BAD_REQUEST:
        db_session.rollback()
        return response
    try:
        db_session.commit()
    except SQLAlchemyError as e:
        db_session.rollback()
        logger.exception("Unexpected problem on commit: {}".format(e))
        response.status_code = http.HTTPStatus.BAD_REQUEST
        response.headers["Content-Type"] = "text/json"
        response.data = {
            "errors": [
                {
                    "code": 4000010,
                    "status": http.HTTPStatus.BAD_REQUEST,
                    "title": "Error handling the request, see server logs for more info",
                }
            ]
        }
    return response


@flask_app.teardown_appcontext
def shutdown_session(exception=None):
    if exception:
        db_session.rollback()
    db_session.remove()


@flask_app.errorhandler(Exception)
def handle_exception(error):
    error_type = type(error)

    # Check if the error is in the error_status_codes dictionary
    if error_type in ERROR_STATUS_CODES:
        status_code = ERROR_STATUS_CODES[error_type].value
        response = jsonify({"error": str(error)})
        response.status_code = status_code
        return response

    # Fallback for unhandled exceptions
    response = jsonify({"error": "An unexpected error occurred."})
    response.status_code = http.HTTPStatus.INTERNAL_SERVER_ERROR
    return response
