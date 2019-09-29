import os

from config import Config
from flask import Flask
from flask_migrate import Migrate
from flask_rebar import Rebar
from flask_sqlalchemy import SQLAlchemy

# Globally accessible libraries
rebar = Rebar()
registry = rebar.create_handler_registry(prefix="/api")
db = SQLAlchemy()
migrate = Migrate()

def create_app(test_config=None) -> Flask:
    """Initialize the core application"""
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_object(Config)
    else:
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)

    # Make models available for sqlalchemy
    from JDISCTF import models

    # Import controllers for flask_rebar
    from JDISCTF.api import auth, users

    db.init_app(app)
    migrate.init_app(app, db)
    rebar.init_app(app)

    return app