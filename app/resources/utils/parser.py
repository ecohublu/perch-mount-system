import functools
import flask
from flask_restx import reqparse
import marshmallow


class SchemaByRequestParser(reqparse.RequestParser):
    arguments: tuple[reqparse.Argument] = ()

    def __init__(
        self,
        argument_class=reqparse.Argument,
        result_class=reqparse.ParseResult,
        trim=False,
        bundle_errors=False,
    ):
        super().__init__(
            argument_class,
            result_class,
            trim,
            bundle_errors,
        )
        self._add_arguments()

    def _add_arguments(self):
        for argument in self.arguments:
            self.add_argument(argument)


class Parser:
    get: reqparse.RequestParser | marshmallow.Schema | None = None
    post: reqparse.RequestParser | marshmallow.Schema | None = None
    patch: reqparse.RequestParser | marshmallow.Schema | None = None
    put: reqparse.RequestParser | marshmallow.Schema | None = None
    detele: reqparse.RequestParser | marshmallow.Schema | None = None


def parse_args(parser: reqparse.RequestParser | marshmallow.Schema):

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if isinstance(parser, reqparse.RequestParser):
                print(parser)
                parsed_args = parser.parse_args()

            elif isinstance(parser, marshmallow.Schema):
                json_data = flask.request.get_json(force=True)
                parsed_args = parser.load(json_data)

            return func(*args, **kwargs, parsed_args=parsed_args)

        return wrapper

    return decorator
