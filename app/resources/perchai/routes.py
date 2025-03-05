import enum
import typing

from app.resources import perchai
from app.resources import Route

_VAR_TYPES = typing.Literal["int", "string", "float", "uuid"]


class VarTypes(enum.Enum):
    INT = "int"
    STRING = "string"
    FLOAT = "float"
    UUID = "uuid"


class RouteVar:
    def __init__(self, name: str, type_: _VAR_TYPES):
        self.name = name
        self.type = type_

    @property
    def param(self) -> str:
        return f"<{self.type}:{self.name}>"


taxon_order = RouteVar(name="taxon_order", type_="int")
section_id = RouteVar(name="section_id", type_="uuid")
perch_mount_id = RouteVar(name="perch_mount_id", type_="uuid")
member_id = RouteVar(name="member_id", type_="uuid")
medium_id = RouteVar(name="medium_id", type_="uuid")
individual_id = RouteVar(name="individual_id", type_="uuid")

ROUTES = [
    Route(
        route="perch_mounts",
        resources=[perchai.PerchMounts],
        children=[
            Route(
                route=perch_mount_id.param,
                resources=[perchai.PerchMount],
            )
        ],
    ),
    Route(
        route="sections",
        resources=[perchai.Sections],
        children=[
            Route(
                route=section_id.param,
                resources=[perchai.Section],
            ),
        ],
    ),
    Route(
        route="media",
        resources=[perchai.Media],
        children=[Route(route=medium_id.param, resources=[perchai.Medium])],
    ),
    Route(
        route="individuals",
        resources=[],
        children=[Route(route=individual_id.param, resources=[perchai.Individual])],
    ),
    Route(
        route="projects",
        resources=[perchai.Projects],
    ),
    Route(
        route="cameras",
        resources=[perchai.Cameras],
    ),
    Route(
        route="event",
        resources=[perchai.Events],
    ),
    Route(
        route="mount_types",
        resources=[perchai.MountTypes],
    ),
    Route(
        route="behaviors",
        resources=[perchai.Behaviors],
    ),
    Route(
        route="members",
        resources=[perchai.Members],
        children=[Route(route=member_id.param, resources=[perchai.Member])],
    ),
    Route(
        route="species",
        resources=[perchai.Species],
        children=[Route(route=taxon_order.param, resources=[perchai.ASpecies])],
    ),
]
