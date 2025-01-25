from flask import Flask
from app.extensions import db, migrate


def create_app(config_object="config.Config") -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_object)

    db.init_app(app)
    migrate.init_app(app, db)

    return app
