from datetime import datetime, date
from flask_restx import reqparse
import uuid

from app.resources.utils import type_funcs
from app.resources.utils import parser
from app.resources.perchai.parsers import (
    media_oper_schema,
    prey_oper_schema,
    schemas,
)


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
    get.add_argument("swapper_ids", type=type_funcs.uuid_split, location="args")

    post = reqparse.RequestParser()
    post.add_argument("perch_mount_id", required=True, type=uuid.UUID)
    post.add_argument("mount_type_id", required=True, type=uuid.UUID)
    post.add_argument("camera_id", required=True, type=uuid.UUID)
    post.add_argument("swapped_date", required=True, type=date.fromisoformat)
    post.add_argument("start_time", required=True, type=datetime.fromisoformat)
    post.add_argument("end_time", required=True, type=datetime.fromisoformat)
    post.add_argument("valid", type=type_funcs.bool_)
    post.add_argument("note", type=str)


class Section(parser.Parser):
    patch = schemas.SectionPatchSchema()


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


class PerchMount(parser.Parser):
    patch = schemas.PerchMountPatchSchema()


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


class MediumFeature(parser.Parser):
    patch = schemas.MediumFeaturePatchSchema()


class Individual(parser.Parser):
    patch = schemas.IndividualPatchSchema()


class IndividualPrey(parser.Parser):
    post = schemas.IndividualPreyPatchSchema()
    patch = schemas.IndividualPreyPostSchema()


class IdentifiedPreys(parser.Parser):
    post = prey_oper_schema.IdentifiedPreySchema(many=True)


class IndividualNote(parser.Parser):
    put = schemas.IndividualNotePutSchema()


class UploadedMedia(parser.Parser):
    post = media_oper_schema.UploadedMediumSchema(many=True)


class DetectedMedia(parser.Parser):
    post = media_oper_schema.DetectedMediumSchema(many=True)


class CheckedMedia(parser.Parser):
    post = media_oper_schema.CheckedMediumSchema(many=True)


class ReviewedMedia(parser.Parser):
    post = media_oper_schema.ReviewedMediumSchema(many=True)


class Members(parser.Parser):
    post = reqparse.RequestParser()
    post.add_argument("gmail", required=True, type=type_funcs.email)
    post.add_argument("user_name", required=True, type=str)
    post.add_argument("first_name", required=True, type=str)
    post.add_argument("last_name", required=True, type=str)
    post.add_argument("position", required=True, type=str)


class Member(parser.Parser):
    get = reqparse.RequestParser()
    get.add_argument("activated", type=type_funcs.bool_)
    patch = schemas.MemberPatchSchema()


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
