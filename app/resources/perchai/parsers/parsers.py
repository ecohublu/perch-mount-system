from app.resources.utils import type_funcs
from app.resources.utils import parser
from datetime import datetime
from flask_restx import reqparse
import uuid


class Species(parser.Parser):
    get = reqparse.RequestParser()
    get.add_argument("taxon_orders", type=type_funcs.int_split, location="args")
    get.add_argument("chinese_common_name", type=type_funcs.str_split, location="args")
    get.add_argument("english_common_name", type=type_funcs.str_split, location="args")
    get.add_argument("scientific_name", type=type_funcs.str_split, location="args")
    get.add_argument("name", type=str, location="args")
    get.add_argument("conservation_status", type=str, location="args")
    get.add_argument("protected", type=type_funcs.bool_, location="args")
    get.add_argument("orders", type=type_funcs.str_split, location="args")
    get.add_argument("families", type=type_funcs.str_split, location="args")
    get.add_argument("codes", type=type_funcs.str_split, location="args")


class Sections(parser.Parser):
    get = reqparse.RequestParser()
    get.add_argument("perch_mount_ids", type=type_funcs.str_split, location="args")
    get.add_argument("swapped_date_from", type=datetime.fromisoformat, location="args")
    get.add_argument("swapped_date_to", type=datetime.fromisoformat, location="args")
    get.add_argument("swapper_ids", type=type_funcs.str_split, location="args")


class PerchMounts(parser.Parser):
    get = reqparse.RequestParser()
    get.add_argument("project_ids", type=type_funcs.uuid_split, location="args")
    get.add_argument("claim_by_ids", type=type_funcs.uuid_split, location="args")
    get.add_argument("habitats", type=type_funcs.str_split, location="args")
    get.add_argument("terminated", type=type_funcs.bool_, location="args")

    post = reqparse.RequestParser()
    post.add_argument("perch_mount_name", required=True, type=str)
    post.add_argument("longitude", required=True, type=float)
    post.add_argument("latitude", required=True, type=float)
    post.add_argument("habitat", required=True, type=str)
    post.add_argument("project_id", required=True, type=uuid.UUID)
    post.add_argument("mount_layer", required=True, type=str)
    post.add_argument("note", type=str)


class Media(parser.Parser):
    get = reqparse.RequestParser()
    get.add_argument("status", required=True, type=str, location="args")
    get.add_argument("perch_mount_ids", type=type_funcs.uuid_split, location="args")
    get.add_argument("section_ids", type=type_funcs.uuid_split, location="args")
    get.add_argument("is_tagged", type=type_funcs.bool_, location="args")
    get.add_argument("ring_number_search", type=str, location="args")
    get.add_argument("prey_status", type=str, location="args")
    get.add_argument("has_prey", type=str, location="args")
    get.add_argument(
        "prey_inaturalist_taxa_ids", type=type_funcs.int_split, location="args"
    )
    get.add_argument(
        "taxon_orders_by_human", type=type_funcs.int_split, location="args"
    )
    get.add_argument("taxon_orders_by_ai", type=type_funcs.int_split, location="args")


class Members(parser.Parser):
    post = reqparse.RequestParser()
    post.add_argument("gmail", required=True, type=type_funcs.email)
    post.add_argument("user_name", required=True, type=str)
    post.add_argument("first_name", required=True, type=str)
    post.add_argument("last_name", required=True, type=str)
    post.add_argument("position", required=True, type=str)


class Projects(parser.Parser):
    post = reqparse.RequestParser()
    post.add_argument("name", required=True, type=str)


class Cameras(parser.Parser):
    post = reqparse.RequestParser()
    post.add_argument("name", required=True, type=str)


class Events(parser.Parser):
    post = reqparse.RequestParser()
    post.add_argument("name", required=True, type=str)


class MountTypes(parser.Parser):
    post = reqparse.RequestParser()
    post.add_argument("name", required=True, type=str)


class Behaviors(parser.Parser):
    post = reqparse.RequestParser()
    post.add_argument("name", required=True, type=str)
