import flask_restx
import uuid

from app.services import perchai as perchai_service
from app.resources.perchai import parsers
import app.resources.utils as resource_utils


class Individual(flask_restx.Resource):
    @resource_utils.parse_json_body_args(parsers.Individual.post)
    def patch(self, individual_id: uuid.UUID):
        return


class IndividualPrey(flask_restx.Resource):
    def post(self, individual_id: uuid.UUID):
        return

    def patch(self, individual_id: uuid.UUID):
        return

    def delete(self, individual_id: uuid.UUID):
        return


class IndividualNote(flask_restx.Resource):
    def put(self, individual_id: uuid.UUID):
        return

    def delete(self, individual_id: uuid.UUID):
        return
