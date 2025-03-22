# app/__init__.py
import os
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from app.db.mysql import db
from app.db.mongodb import mongo
from config import config


def register_extensions(app):
    """Register Flask extensions."""
    db.init_app(app)
    mongo.init_app(app)
    JWTManager(app)
    return None


def register_blueprints(app):
    """Register Flask blueprints."""
    from app.routes.auth import auth_bp
    from app.routes.profile import profile_bp
    from app.routes.analysis import analysis_bp
    from app.routes.routines import routines_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(profile_bp, url_prefix='/api/profile')
    app.register_blueprint(analysis_bp, url_prefix='/api/analysis')
    app.register_blueprint(routines_bp, url_prefix='/api/routines')
    return None


def register_error_handlers(app):
    """Register error handlers."""
    @app.errorhandler(404)
    def not_found(e):
        return {"error": "Not found"}, 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return {"error": "Internal server error"}, 500

    return None


def create_app(config_name=None):
    """Create application factory."""
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'default')

    app = Flask(__name__, static_folder='../static', static_url_path='/')
    CORS(app)
    app.config.from_object(config[config_name])

    register_extensions(app)
    register_blueprints(app)
    register_error_handlers(app)

    # Serve React app
    @app.route('/')
    def serve():
        return app.send_static_file("index.html")

    @app.route('/<path:path>')
    def serve_path(path):
        if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
            return app.send_static_file(path)
        else:
            return app.send_static_file("index.html")

    return app

# app/models/__init__.py
"""Models package."""
from app.models.user import User
from app.models.routine import Routine
# Note: Image model is not imported as it's not a SQLAlchemy model
