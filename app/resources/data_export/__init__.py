import flask_restx
from app.resources import routing

from app.resources.data_export.routes import ROUTES


api = flask_restx.Api(prefix="/api/data")
