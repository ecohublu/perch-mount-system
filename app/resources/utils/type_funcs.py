import uuid
import re

_TRUES = {"true", "1", "yes", "y", "ya", "いいよ"}
_FALSES = {"false", "0", "no", "n", "na", "いや"}
_SEPARATOR = ","


def _split(values: str, type_func):
    return list(map(type_func, values.split(_SEPARATOR)))


def uuid_split(values: str) -> list[uuid.UUID]:
    return _split(values, uuid.UUID)


def int_split(values: str) -> list[int]:
    return _split(values, int)


def str_split(values: str) -> list[str]:
    return values.split(_SEPARATOR)


def bool_(value: str) -> bool:
    if value.lower() in _TRUES:
        return True
    if value.lower() in _FALSES:
        return False


def email(value: str) -> str:
    if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
        raise ValueError("Invalid email address")
    return value
