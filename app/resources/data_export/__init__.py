import flask
import flask_restx
from app.resources import routing
from app.resources.data_export.data import *
from app.resources.data_export.routes import ROUTES

blueprint = flask.Blueprint("data_export", __name__)
api = flask_restx.Api(blueprint)

routes = routing.Routes(ROUTES)
routes.init_api(api)

ns = flask_restx.Namespace("data_export")
api.add_namespace(ns)
