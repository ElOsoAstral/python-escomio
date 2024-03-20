# Packages
from flask import Flask
import os

# Local files
from app.route import health_bp, auth_bp


def create_app():
    flask_app = Flask(__name__, instance_relative_config=True)

    # Get environment, if not defined 'development' will be default
    environment = os.getenv('FLASK_ENV', 'development')

    # App configuration
    if environment == 'production':
        flask_app.config.from_pyfile('production_config.py', silent=True)
    else:
        flask_app.config.from_pyfile('development_config.py', silent=True)

    # Blueprints registry
    flask_app.register_blueprint(auth_bp, url_prefix='/auth')
    flask_app.register_blueprint(health_bp, url_prefix='/health')

    return flask_app
