import flask

from app.services.perchai import species
from app.species_trie import trie


trier = trie.SpeciesTrie(species.get_species())

blueprint = flask.Blueprint("species_trie", __name__)


@blueprint.route("/trie")
def species_prediction():
    phrase = flask.request.args.get("phrase")
    return {"results": trier.search(phrase)}
