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


api = flask_restx.Api(prefix="/api/perchai")
routes = routing.Routes(ROUTES)
routes.init_api(api)
