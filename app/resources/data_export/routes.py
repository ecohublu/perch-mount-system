from app.resources import data_export
from app.resources import routing

ROUTES = [
    routing.Route(
        route="previews",
        resources=[data_export.Data],
    ),
    routing.Route(
        route="email_export",
        resources=[data_export.EmailExports],
    ),
]
