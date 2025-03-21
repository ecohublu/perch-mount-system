import functools
import flask
from flask_restx import reqparse
import marshmallow


class Parser:
    get: reqparse.RequestParser | None = None
    post: reqparse.RequestParser | None = None
    patch: reqparse.RequestParser | None = None
    put: reqparse.RequestParser | None = None
    detele: reqparse.RequestParser | None = None


def parse_args(parser: reqparse.RequestParser):

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            parsed_args = parser.parse_args()
            return func(*args, **kwargs, parsed_args=parsed_args)

        return wrapper

    return decorator


def parse_json_body_args(schema: marshmallow.Schema):

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            json_data = flask.request.get_json(force=True)
            parsed_args = schema.load(json_data)
            return func(*args, **kwargs, parsed_args=parsed_args)

        return wrapper

    return decorator
