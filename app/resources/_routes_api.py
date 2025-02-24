
from typing import List
from collections import defaultdict
import flask_restful


class Route:
    def __init__(self, route: str,resources: List[flask_restful.Resource], children: List["Route"] = []):
        self.route = route
        self.resources = resources
        self.children = children


class Routes:
    _route_map = defaultdict(list)

    def __init__(self, routes: list[Route]):
        self.routes = routes

    def init_api(self, api: flask_restful.Api):
        self._route_map.clear()
        self._find_route_map(self.routes)
        self._add_resources(api, self._route_map)

    def _find_route_map(self, routes: list[Route], parent: str = "/"):
        for route in routes:

            endpoint = f"{parent}{route.route}/"

            for resource in route.resources:

                self._route_map[resource].append(endpoint)

            self._find_route_map(route.children, parent=endpoint)

    def _add_resources(self, api: flask_restful.Api, route_map: dict):
        for resource, endpoints in route_map.items():
            api.add_resource(resource, *endpoints)

