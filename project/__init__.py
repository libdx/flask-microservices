import os

from flask import Flask
from flask_admin import Admin
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
cors = CORS()
admin = Admin(template_mode="bootstrap3")
bcrypt = Bcrypt()


def create_app(script_info=None):
    """Creates and initializes new Flask instance"""

    app = Flask(__name__)

    app_settings = os.getenv("APP_SETTINGS")

    app.config.from_object(app_settings)

    db.init_app(app)
    cors.init_app(app, resources={r"*": {"origins": "*"}})
    bcrypt.init_app(app)
    if os.getenv("FLASK_ENV") == "development":
        admin.init_app(app)

    from project.api import api

    api.init_app(app)

    @app.shell_context_processor
    def ctx():
        return {"app": app, "db": db}

    return app
