import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_seeder import FlaskSeeder
from .config import Config
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_socketio import SocketIO
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

sqlalchemy = SQLAlchemy()
migrate = Migrate(compare_type=True)
bcrypt = Bcrypt()
jwt = JWTManager()
socket_io = SocketIO()
config = Config()
seeder = FlaskSeeder()
"""
Create a flask app instance with given
configuration object, initialize extentions
and register flask blueprints
"""


def create_app(config_obj=None):
    app = Flask(__name__)

    if config_obj is None:
        app.config.from_object(config)
    else:
        app.config.from_object(config_obj)

    # initialize extensions and register blueprints
    initialize_extentions(app)
    register_blueprints(app)

    # Create database tables if they do not exist
    # within flask application context
    with app.app_context():
        sqlalchemy.create_all()

    return app


def initialize_extentions(app):
    jwt.init_app(app)
    bcrypt.init_app(app)
    sqlalchemy.init_app(app)
    migrate.init_app(app, sqlalchemy)
    seeder.init_app(app, sqlalchemy)
    socket_io.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})


def register_blueprints(app):
    from app.admin import admin
    from app.api import api

    app.register_blueprint(admin)
    app.register_blueprint(api)
