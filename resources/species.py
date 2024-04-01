import flask

import cache
import cache.key
import resources
import service.species
from src import pm_resource


class Species(pm_resource.PerchMountResource):
    @cache.cache.cached(make_cache_key=cache.key.key_generate)
    def get(self):
        args = dict(flask.request.args)
        results = service.species.get_species(**args)
        return {"species": [result.to_json() for result in results]}


class ASpecies(pm_resource.PerchMountResource):
    @cache.cache.cached(make_cache_key=cache.key.key_generate)
    def get(self, taxon_order: int):
        result = service.species.get_species_by_taxon_order(taxon_order)
        return result.to_json()
