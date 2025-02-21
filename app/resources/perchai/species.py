import flask
import flask_restful

from app.services import perchai as perchai_service


class Species(flask_restful.Resource):
    def get(self):
        args = dict(flask.request.args)
        species_filter = perchai_service.utils.query_filter.SpeciesFilter(**args)
        species = perchai_service.species.get_species_by_filter(species_filter)
        return
