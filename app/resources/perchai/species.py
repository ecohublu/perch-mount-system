import flask_restx

import app.services.perchai as perchai_service
from app.resources.perchai import parsers
import app.resources.utils as resource_utils
from app.error_handler import errors
from app import model


class Species(flask_restx.Resource):
    @resource_utils.parse_args(parsers.Species.get)
    def get(self, parsed_args):
        species_filter = perchai_service.utils.query_filter.SpeciesFilter(**parsed_args)
        species = perchai_service.species.get_species_by_filter(species_filter)
        return [s.to_dict() for s in species]


class ASpecies(flask_restx.Resource):
    def get(self, taxon_order: int):
        species = perchai_service.species.get_species_by_taxon_order(taxon_order)

        if species is None:
            raise errors.ResourceNotFoundError(model.Species.__name__)

        return species.to_dict()
