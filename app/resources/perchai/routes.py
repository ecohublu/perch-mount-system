from app.resources import perchai
from app.resources import routing


_taxon_order = routing.RouteVar(name="taxon_order", type_="int")
_section_id = routing.RouteVar(name="section_id", type_="uuid")
_perch_mount_id = routing.RouteVar(name="perch_mount_id", type_="uuid")
_member_id = routing.RouteVar(name="member_id", type_="uuid")
_medium_id = routing.RouteVar(name="medium_id", type_="uuid")
_individual_id = routing.RouteVar(name="individual_id", type_="uuid")

ROUTES = [
    routing.Route(
        route="perch_mounts",
        resources=[perchai.PerchMounts],
        children=[
            routing.Route(
                route=_perch_mount_id.param,
                resources=[perchai.PerchMount],
                children=[
                    routing.Route(
                        route="activation",
                        resources=[perchai.PerchMountActivation],
                    ),
                    routing.Route(
                        route="pending_counts",
                        resources=[perchai.PerchMountPendingCounts],
                    ),
                ],
            ),
            routing.Route(
                route="pending_counts",
                resources=[perchai.PerchMountsPendingCounts],
            ),
        ],
    ),
    routing.Route(
        route="sections",
        resources=[perchai.Sections],
        children=[
            routing.Route(
                route=_section_id.param,
                resources=[perchai.Section],
            ),
        ],
    ),
    routing.Route(
        route="media",
        resources=[perchai.Media],
        children=[routing.Route(route=_medium_id.param, resources=[perchai.Medium])],
    ),
    routing.Route(
        route="individuals",
        resources=[],
        children=[
            routing.Route(
                route=_individual_id.param,
                resources=[perchai.Individual],
                children=[
                    routing.Route(route="prey", resources=[perchai.IndividualPrey]),
                    routing.Route(route="note", resources=[perchai.IndividualNote]),
                ],
            ),
        ],
    ),
    routing.Route(
        route="projects",
        resources=[perchai.Projects],
    ),
    routing.Route(
        route="cameras",
        resources=[perchai.Cameras],
    ),
    routing.Route(
        route="event",
        resources=[perchai.Events],
    ),
    routing.Route(
        route="mount_types",
        resources=[perchai.MountTypes],
    ),
    routing.Route(
        route="behaviors",
        resources=[perchai.Behaviors],
    ),
    routing.Route(
        route="members",
        resources=[perchai.Members],
        children=[
            routing.Route(
                route=_member_id.param,
                resources=[perchai.Member],
                children=[
                    routing.Route(
                        route="block",
                        resources=[perchai.MemberBlock],
                    ),
                    routing.Route(
                        route="activation",
                        resources=[perchai.MemberActivation],
                    ),
                ],
            ),
        ],
    ),
    routing.Route(
        route="species",
        resources=[perchai.Species],
        children=[
            routing.Route(route=_taxon_order.param, resources=[perchai.ASpecies])
        ],
    ),
    routing.Route(
        route="uploaded_media",
        resources=[perchai.UploadedMedia],
    ),
    routing.Route(
        route="detected_media",
        resources=[perchai.DetectedMedia],
    ),
    routing.Route(
        route="checked_media",
        resources=[perchai.CheckedMedia],
    ),
    routing.Route(
        route="reviewed_media",
        resources=[perchai.ReviewedMedia],
    ),
    routing.Route(
        route="identified_preys",
        resources=[perchai.IdentifiedPreys],
    ),
]
