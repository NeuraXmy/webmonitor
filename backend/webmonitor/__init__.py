from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from config import config_map
from flask_migrate import Migrate

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(config_map["development"])
    register_database(app)
    register_blueprints(app)
    register_plugin(app)
    return app


def register_database(app):
    db.init_app(app)
    Migrate(app, db)


def register_blueprints(app):
    from webmonitor.auth import auth_bp
    app.register_blueprint(auth_bp)
    from webmonitor.watch import watch_bp
    app.register_blueprint(watch_bp)
    from webmonitor.space import space_bp
    app.register_blueprint(space_bp)
    from webmonitor.user import user_bp
    app.register_blueprint(user_bp)


def register_plugin(app):
    apply_cors(app)


def apply_cors(app):
    cors = CORS()
    cors.init_app(app, resources={"/*": {"origins": "*"}})
