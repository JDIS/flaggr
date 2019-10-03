"""The flask app"""

import os

from config import Config
from flask import Flask
from flask_migrate import Migrate
from flask_rebar import Rebar
from flask_sqlalchemy import SQLAlchemy

# Globally accessible libraries
REBAR = Rebar()
REGISTRY = REBAR.create_handler_registry(prefix="/api")
DB = SQLAlchemy()
MIGRATE = Migrate()


def create_app(test_config=None) -> Flask:
    """Initialize the core application"""

    app = Flask(__name__, instance_relative_config=True)

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
