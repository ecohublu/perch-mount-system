import flask_restx
import uuid

from app.services import perchai as perchai_service
from app.resources.perchai import parsers
import app.resources.utils as resource_utils
from app.error_handler import errors
from app import model


class Individual(flask_restx.Resource):
    @resource_utils.parse_json_body_args(parsers.Individual.patch)
    def patch(self, individual_id: uuid.UUID, parsed_args: dict):
        print(parsed_args)

        individual = perchai_service.individuals.update_individual(
            individual_id, parsed_args
        )

        if not individual:
            raise errors.ResourceNotFoundError(model.Individuals.__name__)

        return individual.to_dict()


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
