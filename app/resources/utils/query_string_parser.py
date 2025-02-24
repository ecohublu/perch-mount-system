import flask
import functools
import uuid

TRUES = {"true", "1", "yes", "y", "ya", "いいよ"}
FALSES = {"false", "0", "no", "n", "na", "ダメ"}
SEPARATOR = ","


def _to_list(values: str, type_func):
    return list(map(type_func, values.split(SEPARATOR)))


class StringQueryTypeCoverter:

    def __init__(self, typing: dict):
        self.typing = typing

    def convert(self, field: str, value: str):
        return self.typing[field](value)

    @staticmethod
    def to_bool(value: str) -> list:
        if value in TRUES:
            return True
        if value in FALSES:
            return False

    @staticmethod
    def to_uuid_list(values: str) -> list[uuid.UUID]:
        return _to_list(values, uuid.UUID)

    @staticmethod
    def to_int_list(values: str) -> list[int]:
        return _to_list(values, int)

    @staticmethod
    def to_str_list(values: str) -> list[str]:
        return values.split(SEPARATOR)


def parse_args(converter: "StringQueryTypeCoverter"):

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            parsed_args = {}
            response_args = dict(flask.request.args)
            for field, value in response_args.items():
                parsed_args[field] = converter.convert(field, value)
            return func(*args, **kwargs, parsed_args=parsed_args)

        return wrapper

    return decorator
