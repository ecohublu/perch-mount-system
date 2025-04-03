from datetime import datetime
from flask_restx import reqparse

from app.resources.utils import parser
from app.resources.utils import type_funcs


_SHARE_DATA_ARGUMENTS = [
    reqparse.Argument(
        "field_sets",
        type=type_funcs.str_split,
        location="args",
        required=True,
    ),
    reqparse.Argument("projects", type=type_funcs.uuid_split, location="args"),
    reqparse.Argument("perch_mounts", type=type_funcs.uuid_split, location="args"),
    reqparse.Argument("habitats", type=type_funcs.str_split, location="args"),
    reqparse.Argument("cameras", type=type_funcs.uuid_split, location="args"),
    reqparse.Argument("mount_types", type=type_funcs.uuid_split, location="args"),
    reqparse.Argument(
        "medium_datetime_from",
        type=datetime.fromisoformat,
        location="args",
    ),
    reqparse.Argument(
        "medium_datetime_to",
        type=datetime.fromisoformat,
        location="args",
    ),
    reqparse.Argument(
        "taxon_orders_by_ai",
        type=type_funcs.int_split,
        location="args",
    ),
    reqparse.Argument(
        "taxon_orders_by_human",
        type=type_funcs.int_split,
        location="args",
    ),
    reqparse.Argument("has_prey", type=type_funcs.bool_, location="args"),
    reqparse.Argument(
        "inaturalist_taxa_ids",
        type=type_funcs.int_split,
        location="args",
    ),
    reqparse.Argument("tagged", type=type_funcs.bool_, location="args"),
    reqparse.Argument("included_unreviewed", type=type_funcs.bool_, location="args"),
]


class PreviewsGetSchmea(parser.SchemaByRequestParser):
    arguments = _SHARE_DATA_ARGUMENTS


class EmailExportPostSchmea(parser.SchemaByRequestParser):
    arguments: list[reqparse.Argument] = [
        argument for argument in _SHARE_DATA_ARGUMENTS
    ]
    arguments.append(
        reqparse.Argument(
            "mail_to",
            type=type_funcs.email,
            location="arg",
        )
    )


class Previews(parser.Parser):
    get = PreviewsGetSchmea()


class EmailExport(parser.Parser):
    post = EmailExportPostSchmea()
