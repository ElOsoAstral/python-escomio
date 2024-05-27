import logging
import os

from flask import Flask
from flask_cors import CORS

# Local files
from app.route import health_bp, auth_bp, rasa_bp
from app.service import FirebaseService
from app.connection import RedisConnection
from app.respository import initialize_database

# Global variables
firebase_app = None
firebase_admin = None
redis_connection = None


def create_app():

    # Initializes the Flask application
    app = Flask(__name__, instance_relative_config=True)

    try:
        # This allows access from any origin. To restrict to certain domain replace "*" with url
        CORS(app)
        app.config['CORS_HEADERS'] = 'Content-Type'

        # Configuration loading
        environment = os.getenv('FLASK_ENV', 'development')
        app.config.from_pyfile(f'{environment}_config.py', silent=True)

        # Blueprints registry
        app.register_blueprint(auth_bp, url_prefix='/auth')
        app.register_blueprint(health_bp, url_prefix='/health')
        app.register_blueprint(rasa_bp, url_prefix='/rasa')

        # Activates all level logging
        app.logger.setLevel(logging.DEBUG)

        # Initializes firebase services
        FirebaseService.init_app(app)

        # Intializes redis services
        with app.app_context():
            initialize_database(RedisConnection.init_connection())

        return app

    except Exception as e:
        app.logger.error(f"Unable to create flask application: {e}")
        raise Exception("Flask services are unavailable") from e
