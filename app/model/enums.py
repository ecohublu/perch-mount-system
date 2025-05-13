import enum
import typing


class Habitats(enum.Enum):
    NATURAL = "natural"
    ARTIFICIAL = "artificial"
    SOLAR_PANEL = "solar_panel"


class MountLayers(enum.Enum):
    LOW = "lower"
    MIDDLE = "middle"
    HIGH = "high"


class MediaStatus(enum.Enum):
    UNDETECTED = "undetected"
    UNCHECKED = "unchecked"
    UNREVIEWED = "unreviewed"
    REVIEWED = "reviewed"
    ACCIDENTAL = "accidental"


class PreyStatus(enum.Enum):
    UNCHECKED = "unchecked"
    UNIDENTIFIED = "unidentified"
    NO_PREY = "no_prey"
    IDENTIFIED = "identified"


class MediaTypes(enum.Enum):
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


class ContributionType(enum.Enum):
    REVIEW = "review"
    EMPTY_CHECK = "empty_check"
    IDENTIFY_PREY = "identify_prey"


class ConservationStatus(enum.Enum):
    I = "I"
    II = "II"
    III = "III"


def validate_enums(
    values: typing.List[str | enum.Enum],
    enum_type: typing.Type[enum.Enum] = None,
):
    not_in_enum = []
    for v in values:
        if not isinstance(v, enum_type):
            not_in_enum.append(v)
    if not_in_enum:
        raise ValueError(
            f"Invalid status: {",".join(not_in_enum)}. Must be one of {[e.value for e in enum_type]}"
        )


def validate_enum(
    value: typing.Union[str | enum.Enum],
    enum_type: typing.Type[enum.Enum] = None,
):
    try:
        enum_type(value)
    except ValueError:
        raise ValueError(
            f"Invalid status: {value}. Must be one of {[e.value for e in enum_type]}"
        )
