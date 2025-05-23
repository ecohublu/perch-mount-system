from app.resources.features import features
from app.resources import routing

ROUTES = [
    routing.Route(
        route="features",
        resources=[features.Features],
    ),
]
