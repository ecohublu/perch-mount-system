from flask_restx import reqparse

from app.resources.utils import parser
from app.resources.utils import type_funcs


class PreviewsGetSchmea(parser.SchemaByRequestParser):
    arguments = (
        reqparse.Argument(
            "field_sets",
            type=type_funcs.str_split,
            location="args",
            required=True,
        ),
    )


class EmailExportPostSchmea(parser.SchemaByRequestParser):
    arguments = (
        reqparse.Argument(
            "field_sets",
            type=type_funcs.str_split,
            location="args",
            required=True,
        ),
    )


class Previews(parser.Parser):
    get = PreviewsGetSchmea()


class EmailExport(parser.Parser):
    post = EmailExportPostSchmea()
