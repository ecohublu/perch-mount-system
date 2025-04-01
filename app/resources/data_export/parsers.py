from flask_restx import reqparse

from app.resources.utils import parser
from app.resources.utils import type_funcs


class Previews(parser.Parser):
    get = reqparse.RequestParser()
    get.add_argument(
        "field_sets",
        type=type_funcs.str_split,
        location="args",
        required=True,
    )


class EmailExport(parser.Parser):
    post = reqparse.RequestParser()
    post.add_argument(
        "field_sets",
        type=type_funcs.str_split,
        location="args",
        required=True,
    )
    post.add_argument("mail_to", type=type_funcs.email, location="args")
