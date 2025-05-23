import flask
import flask_restx
from app.resources import routing
from app.resources.features import *
from app.resources.features.routes import ROUTES

blueprint = flask.Blueprint("featrues", __name__)
api = flask_restx.Api(blueprint)

routes = routing.Routes(ROUTES)
routes.init_api(api)

ns = flask_restx.Namespace("features")
api.add_namespace(ns)
