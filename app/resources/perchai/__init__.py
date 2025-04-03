import flask
import flask_restx
from app.resources import routing

from app.resources.perchai.species import *
from app.resources.perchai.sections import *
from app.resources.perchai.perch_mounts import *
from app.resources.perchai.options import *
from app.resources.perchai.members import *
from app.resources.perchai.media import *
from app.resources.perchai.individuals import *
from app.resources.perchai.routes import ROUTES

blueprint = flask.Blueprint("perchai", __name__)
api = flask_restx.Api(blueprint)

routes = routing.Routes(ROUTES)
routes.init_api(api)

ns = flask_restx.Namespace("perchai")
api.add_namespace(ns)
