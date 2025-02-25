import flask_restful
from app import resources

from app.resources.perchai.species import *
from app.resources.perchai.sections import *
from app.resources.perchai.perch_mounts import *
from app.resources.perchai.options import *
from app.resources.perchai.routes import ROUTES


api = flask_restful.Api()
routes = resources.Routes(ROUTES)
routes.init_api(api)
