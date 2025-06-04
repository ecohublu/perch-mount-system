import flask_restx
import flask_jwt_extended
import uuid

from app.services import perchai as perchai_service
import app.resources.perchai.utils as perchai_utils
from app.resources.perchai import parsers
import app.resources.utils as resource_utils


class Individuals(flask_restx.Resource):
    @resource_utils.parse_args(parsers.Individuals.get)
    def get(self, parsed_args):
        filter = perchai_service.utils.query_filter.IndividualsFilter(**parsed_args)
        individuals = perchai_service.individuals.get_individuals_by_filter(filter)
        return [individual.to_dict() for individual in individuals]


class Individual(flask_restx.Resource):
    @flask_jwt_extended.jwt_required()
    @resource_utils.parse_args(parsers.Individual.patch)
    def patch(self, individual_id: uuid.UUID, parsed_args: dict):
        perchai_service.individuals.update_individual(individual_id, parsed_args)
        individual = perchai_service.individuals.get_individual_by_id(individual_id)
        return individual.to_dict()


class IndividualPrey(flask_restx.Resource):
    @flask_jwt_extended.jwt_required()
    @resource_utils.parse_args(parsers.IndividualPrey.post)
    def post(self, individual_id: uuid.UUID, parsed_args: dict):
        perchai_service.individuals.add_prey(individual_id, parsed_args)
        individual = perchai_service.individuals.get_individual_by_id(individual_id)
        return individual.to_dict()

    @flask_jwt_extended.jwt_required()
    @resource_utils.parse_args(parsers.IndividualPrey.patch)
    def patch(self, individual_id: uuid.UUID, parsed_args: dict):
        perchai_service.individuals.update_prey(individual_id, parsed_args)
        individual = perchai_service.individuals.get_individual_by_id(individual_id)
        return individual.to_dict()

    @flask_jwt_extended.jwt_required()
    def delete(self, individual_id: uuid.UUID):
        perchai_service.individuals.delete_prey(individual_id)
        return perchai_utils.delete_successed(individual_id)


class IdentifiedPreys(flask_restx.Resource):
    @flask_jwt_extended.jwt_required()
    @resource_utils.parse_args(parsers.IdentifiedPreys.post)
    def post(self, parsed_args):
        perchai_service.individuals.add_identified_preys(parsed_args)
        return


class IndividualNote(flask_restx.Resource):
    @flask_jwt_extended.jwt_required()
    @resource_utils.parse_args(parsers.IndividualNote.put)
    def put(self, individual_id: uuid.UUID, parsed_args: dict):
        perchai_service.individuals.upsert_note(individual_id, parsed_args["note"])
        individual = perchai_service.individuals.get_individual_by_id(individual_id)
        return individual.to_dict()

    @flask_jwt_extended.jwt_required()
    def delete(self, individual_id: uuid.UUID):
        perchai_service.individuals.remove_note(individual_id)
        individual = perchai_service.individuals.get_individual_by_id(individual_id)
        return individual.to_dict()
