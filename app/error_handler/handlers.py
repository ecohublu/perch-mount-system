import flask
from app.error_handler import errors

blueprint = flask.Blueprint("error_handlers", __name__)


@blueprint.app_errorhandler(errors.NotFoundError)
def not_found(e: errors.NotFoundError):
    return e.json_response()


@blueprint.app_errorhandler(errors.StringQueryMissingError)
def string_query_missing(e: errors.StringQueryMissingError):
    return e.json_response()