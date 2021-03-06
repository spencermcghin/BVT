from flask import Flask
from flask_bootstrap import Bootstrap

# local imports
from config import app_config


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    Bootstrap(app)

    from app import models

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    return app