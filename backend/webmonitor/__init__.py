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
    from webmonitor.bookmark import bookmark_bp
    app.register_blueprint(bookmark_bp)


def register_plugin(app):
    apply_cors(app)
    apply_json_provider(app)
    apply_exception_handler(app)
    apply_logger(app)


def apply_cors(app):
    cors = CORS()
    cors.init_app(app, resources={"/*": {"origins": "*"}})


def apply_json_provider(app):
    from webmonitor.utils.json_provider import CustomJSONProvider
    app.json = CustomJSONProvider(app)


def apply_exception_handler(app):
    from webmonitor.utils.error import ErrorCode
    from webmonitor.utils.error import APIException

    @app.errorhandler(APIException)
    def handle_api_exception(ex: APIException):
        return ex.error_code.to_response(msg=ex.msg)
    
    @app.errorhandler(Exception)
    def handle_exception(ex):
        import traceback
        tb_msg = traceback.format_exception(type(ex), ex, ex.__traceback__)
        app.logger.error(f"Unhandled Exception Ocurred: {ex}\n" + "".join(tb_msg))

        from sqlalchemy.exc import SQLAlchemyError
        if isinstance(ex, SQLAlchemyError):
            if db.session.is_active:
                app.logger.error("Database Session is active, rollback.")
                db.session.rollback()
            else:
                app.logger.error("Database Session is not active, rollback failed.")

        return ErrorCode.INTERNAL_SERVER_ERROR.to_response(msg=f"Unhandled Exception Ocurred: {ex}")
    

def apply_logger(app):
    pass