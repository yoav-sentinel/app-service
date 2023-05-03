from flask import Flask

from api.endpoints.app import app_bp
from config import UPLOAD_FOLDER, MAX_CONTENT_LENGTH, configure_logging

logger = configure_logging('flask')


def create_flask_app():
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
    app.debug = True

    app.register_blueprint(app_bp)
    return app


flask_app = create_flask_app()
