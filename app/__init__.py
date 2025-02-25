from flask import Flask
from app import model
from app.extensions import db, migrate
from app.error_handler import blueprint as error_handler_blueprint
from app.resources import perchai

def create_app(config_object="config.Config") -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_object)

    db.init_app(app)
    migrate.init_app(app, db)
    perchai.api.init_app(app)
    
    app.register_blueprint(error_handler_blueprint)

    return app
