import enum


class Habitats(enum.Enum):
    NATURAL = "natural"
    ARTIFICIAL = "artificial"
    SOLAR_PANEL = "solar_panel"


class MountLayers(enum.Enum):
    LOW = "lower"
    MIDDLE = "middle"
    HIGH = "high"


class MediaType(enum.Enum):
    IMAGE = "image"
    VIDEO = "video"


class Positions(enum.Enum):
    PROFESSOR = "professor"
    POSTDPC = "postdoc"
    DOCTOR = "doctor"
    MASTER = "master"
    UNDERGRAD = "undergrad"
    ASSISTANT = "assistant"
    PART_TIME = "part_time"


class ConservationStatus(enum.Enum):
    I = "I"
    II = "II"
    III = "III"
