import flask_restful

import app.services.perchai as perchai_service
import app.resources.perchai.string_query_converters as sq_converters
import app.resources.utils as res_utils


class Species(flask_restful.Resource):
    @res_utils.parse_args(sq_converters.species)
    def get(self, parsed_args):
        species_filter = perchai_service.utils.query_filter.SpeciesFilter(**parsed_args)
        species = perchai_service.species.get_species_by_filter(species_filter)
        return [s.to_dict() for s in species]


class ASpecies(flask_restful.Resource):
    def get(self, taxon_order: int):
        species = perchai_service.species.get_species_by_taxon_order(taxon_order)
        return species.to_dict()
