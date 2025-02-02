import enum
from app.model import enums as model_enums


def _get_enums_values(enum_: enum.Enum) -> list[str]:
    return [option.value for option in enum_]


def get_habitats() -> list[str]:
    return _get_enums_values(model_enums.Habitats)


def get_mount_layers() -> list[str]:
    return _get_enums_values(model_enums.MountLayers)


def get_media_status() -> list[str]:
    return _get_enums_values(model_enums.MediaStatus)


def get_media_types() -> list[str]:
    return _get_enums_values(model_enums.MediaTypes)


def get_positions() -> list[str]:
    return _get_enums_values(model_enums.Positions)
