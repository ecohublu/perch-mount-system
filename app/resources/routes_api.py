from collections import defaultdict
import flask_restful


class PerchMountApi(flask_restful.Api):
    _route_map = defaultdict(list)

    def __init__(self, routes):
        super().__init__()
        self.routes = routes

    def init_resources(self):
        self._route_map.clear()
        self._find_route_map(self.routes)
        self._add_resources(self._route_map)

    def _find_route_map(self, routes: list[dict], parent: str = "/"):
        for route in routes:

            endpoint = f"{parent}{route['route']}/"

            for resource in route["resources"]:

                self._route_map[resource].append(endpoint)

            self._find_route_map(route["children"], parent=endpoint)

    def _add_resources(self, route_map: dict):
        for resource, endpoints in route_map.items():
            self.add_resource(resource, *endpoints)
