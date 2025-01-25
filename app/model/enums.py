import enum


class Habitats(enum.Enum):
    NATURAL = "natural"
    ARTIFICIAL = "artificial"
    SOLAR_PANEL = "solar_panel"


class MediaType(enum.Enum):
    IMAGE = "image"
    VIDEO = "video"
