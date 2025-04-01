from collections import defaultdict
import enum
import flask_restx
import typing


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


class Route:
    def __init__(
        self,
        route: str,
        resources: typing.List[flask_restx.Resource],
        children: typing.List["Route"] = [],
    ):
        self.route = route
        self.resources = resources
        self.children = children


class Routes:
    _route_map = defaultdict(list)

    def __init__(self, routes: list[Route]):
        self.routes = routes

    def init_api(self, api: flask_restx.Api):
        self._route_map.clear()
        self._find_route_map(self.routes)
        self._add_resources(api, self._route_map)

    def _find_route_map(self, routes: list[Route], parent: str = "/"):
        for route in routes:
            endpoint = f"{parent}{route.route}/"

            for resource in route.resources:
                self._route_map[resource].append(endpoint)

            self._find_route_map(route.children, parent=endpoint)

    def _add_resources(self, api: flask_restx.Api, route_map: dict):
        for resource, endpoints in route_map.items():
            api.add_resource(resource, *endpoints)
