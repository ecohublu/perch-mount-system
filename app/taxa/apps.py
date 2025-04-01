import flask

from app.services.perchai import species
from app.taxa import trie


trier = trie.SpeciesTrie(species.get_species())

blueprint = flask.Blueprint("species_trie", __name__)


@blueprint.route("/name_predictions")
def species_prediction():
    phrase = flask.request.args.get("phrase")
    return {"results": trier.search(phrase)}
