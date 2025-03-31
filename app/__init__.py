from flask import Flask
import flask_cors
from app import model
from app.extensions import db, migrate, jwt
from app.error_handler import blueprint as error_handler_blueprint
from app.login import blueprint as login_blueprint
from app.species_trie import blueprint as trie_blueprint
from app.resources import perchai


def create_app(config_object="config.Config") -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_object)

    flask_cors.CORS(app)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    perchai.api.init_app(app)

    app.register_blueprint(error_handler_blueprint)
    app.register_blueprint(login_blueprint)
    app.register_blueprint(trie_blueprint)

    return app
