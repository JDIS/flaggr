import os

from flask import Flask
from config import Config
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_object(Config)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)

    # Setup database
    db = SQLAlchemy(app)
    migrate = Migrate(app, db)

    # Ici on devrait caller des app.register_blueprints pour chaque entité / pages et pages d'erreurs. Example : 
    # On délegue la création des routes aux blueprintes

    from JDISCTF.auth import auth
    app.register_blueprint(auth)

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app