"""The flask app"""

import os
from functools import partial

from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_rebar import Rebar
from flask_sqlalchemy import SQLAlchemy

from config import Config
# Globally accessible libraries
from JDISCTF.flask_login_authenticator import register_authenticators

DB = SQLAlchemy()
MIGRATE = Migrate()
REBAR = Rebar()
LOGIN_MANAGER = LoginManager()
REGISTRY = REBAR.create_handler_registry(prefix="/api")

# make columns non-nullable by default, most of them should be
DB.Column = partial(DB.Column, nullable=False)

#register authenticator for Swagger
register_authenticators(REGISTRY)


def create_app(test_config=None) -> Flask:
    """Initialize the core application"""

    app = Flask(__name__, instance_relative_config=True)

    CORS(app)

    if test_config is None:
        app.config.from_object(Config)
    else:
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)

    register_extensions(app)

    return app


def register_extensions(app):
    """Register the various flask extensions used by the app"""

    DB.init_app(app)
    MIGRATE.init_app(app, DB)
    REBAR.init_app(app)
    LOGIN_MANAGER.init_app(app)
