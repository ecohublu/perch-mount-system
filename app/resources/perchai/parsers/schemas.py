from datetime import datetime, date
from flask_restx import reqparse
import marshmallow
import uuid

from app.resources.utils import parser
from app.resources.utils import type_funcs


class ProjectsPostSchema(parser.SchemaByRequestParser):
    arguments = (reqparse.Argument("name", required=True, type=str),)


class SectionsGetSchema(parser.SchemaByRequestParser):
    arguments = (
        reqparse.Argument(
            "perch_mount_ids",
            type=type_funcs.str_split,
            location="args",
        ),
        reqparse.Argument(
            "swapped_date_from",
            type=datetime.fromisoformat,
            location="args",
        ),
        reqparse.Argument(
            "swapped_date_to",
            type=datetime.fromisoformat,
            location="args",
        ),
        reqparse.Argument("swapper_ids", type=type_funcs.uuid_split, location="args"),
    )


class SectionPostSchem(parser.SchemaByRequestParser):
    arguments = (
        reqparse.Argument("perch_mount_id", required=True, type=uuid.UUID),
        reqparse.Argument("mount_type_id", required=True, type=uuid.UUID),
        reqparse.Argument("camera_id", required=True, type=uuid.UUID),
        reqparse.Argument("swapped_date", required=True, type=date.fromisoformat),
        reqparse.Argument("start_time", required=True, type=datetime.fromisoformat),
        reqparse.Argument("end_time", required=True, type=datetime.fromisoformat),
        reqparse.Argument("valid", type=type_funcs.bool_),
        reqparse.Argument("note", type=str),
    )


class SectionPatchSchema(marshmallow.Schema):
    mount_type_id = marshmallow.fields.UUID()
    camera_id = marshmallow.fields.UUID()
    note = marshmallow.fields.String()


class PerchMountsGetSchema(parser.SchemaByRequestParser):
    arguments = (
        reqparse.Argument("project_ids", type=type_funcs.uuid_split, location="args"),
        reqparse.Argument("claim_by_ids", type=type_funcs.uuid_split, location="args"),
        reqparse.Argument("habitats", type=type_funcs.str_split, location="args"),
        reqparse.Argument("terminated", type=type_funcs.bool_, location="args"),
    )


class PerchMountsPostSchema(parser.SchemaByRequestParser):
    arguments = (
        reqparse.Argument("perch_mount_name", required=True, type=str),
        reqparse.Argument("longitude", required=True, type=float),
        reqparse.Argument("latitude", required=True, type=float),
        reqparse.Argument("habitat", required=True, type=str),
        reqparse.Argument("project_id", required=True, type=uuid.UUID),
        reqparse.Argument("mount_layer", required=True, type=str),
        reqparse.Argument("note", type=str),
    )


class PerchMountPatchSchema(marshmallow.Schema):
    longitude = marshmallow.fields.UUID()
    latitude = marshmallow.fields.UUID()
    habitat = marshmallow.fields.String()
    claim_by_id = marshmallow.fields.UUID()
    mount_layer = marshmallow.fields.String()
    terminated = marshmallow.fields.String()
    is_priority = marshmallow.fields.Boolean()
    note = marshmallow.fields.String()


class MembersPostSchema(parser.SchemaByRequestParser):
    arguments = (
        reqparse.Argument("gmail", required=True, type=type_funcs.email),
        reqparse.Argument("user_name", required=True, type=str),
        reqparse.Argument("first_name", required=True, type=str),
        reqparse.Argument("last_name", required=True, type=str),
        reqparse.Argument("position", required=True, type=str),
    )


class MemberPatchSchema(marshmallow.Schema):
    first_name = marshmallow.fields.String()
    last_name = marshmallow.fields.String()
    position = marshmallow.fields.String()


class MediaGetSchema(parser.SchemaByRequestParser):
    arguments = (
        reqparse.Argument("status", required=True, type=str, location="args"),
        reqparse.Argument(
            "perch_mount_ids",
            type=type_funcs.uuid_split,
            location="args",
        ),
        reqparse.Argument("section_ids", type=type_funcs.uuid_split, location="args"),
        reqparse.Argument("is_tagged", type=type_funcs.bool_, location="args"),
        reqparse.Argument("ring_number_search", type=str, location="args"),
        reqparse.Argument("prey_status", type=str, location="args"),
        reqparse.Argument("has_prey", type=str, location="args"),
        reqparse.Argument(
            "prey_inaturalist_taxa_ids",
            type=type_funcs.int_split,
            location="args",
        ),
        reqparse.Argument(
            "taxon_orders_by_human",
            type=type_funcs.int_split,
            location="args",
        ),
        reqparse.Argument(
            "taxon_orders_by_ai",
            type=type_funcs.int_split,
            location="args",
        ),
    )


class MediaPatchSchema(marshmallow.Schema):
    fearured_by_id = marshmallow.fields.UUID()
    behavior_id = marshmallow.fields.UUID()
    event_id = marshmallow.fields.UUID()


class MediumFeaturePatchSchema(marshmallow.Schema):
    featured_by = marshmallow.fields.UUID()
    event_id = marshmallow.fields.UUID()


class IndividualPatchSchema(marshmallow.Schema):
    taxon_order_by_human = marshmallow.fields.Integer()
    box_xmin = marshmallow.fields.Float()
    box_xmax = marshmallow.fields.Float()
    box_ymin = marshmallow.fields.Float()
    box_ymax = marshmallow.fields.Float()


class IndividualNotePatchSchema(marshmallow.Schema):
    note = marshmallow.fields.String()


class IndividualPreyPatchSchema(marshmallow.Schema):
    inaturalist_taxa_id = marshmallow.fields.Integer()
    identifier_id = marshmallow.fields.Integer()


class IndividualPreyPostSchema(marshmallow.Schema):
    inaturalist_taxa_id = marshmallow.fields.Integer()
    identifier_id = marshmallow.fields.Integer()


class IndividualNotePutSchema(marshmallow.Schema):
    note = marshmallow.fields.String()


class IndividualTagPatchSchema(marshmallow.Schema):
    is_tagged = marshmallow.fields.Boolean()
    has_ring = marshmallow.fields.Boolean()
    ring_number = marshmallow.fields.String()


class SpeciesGetSchema(parser.SchemaByRequestParser):
    arguments = (
        reqparse.Argument("taxon_orders", type=type_funcs.int_split, location="args"),
        reqparse.Argument(
            "chinese_common_name",
            type=type_funcs.str_split,
            location="args",
        ),
        reqparse.Argument(
            "english_common_name",
            type=type_funcs.str_split,
            location="args",
        ),
        reqparse.Argument(
            "scientific_name",
            type=type_funcs.str_split,
            location="args",
        ),
        reqparse.Argument("name", type=str, location="args"),
        reqparse.Argument("conservation_status", type=str, location="args"),
        reqparse.Argument("protected", type=type_funcs.bool_, location="args"),
        reqparse.Argument("orders", type=type_funcs.str_split, location="args"),
        reqparse.Argument("families", type=type_funcs.str_split, location="args"),
        reqparse.Argument("codes", type=type_funcs.str_split, location="args"),
    )


class CamerasPostSchema(parser.SchemaByRequestParser):
    arguments = (reqparse.Argument("name", required=True, type=str),)


class EventsPostSchema(parser.SchemaByRequestParser):
    arguments = (reqparse.Argument("name", required=True, type=str),)


class MountTypesPostSchema(parser.SchemaByRequestParser):
    arguments = (reqparse.Argument("name", required=True, type=str),)


class BehaviorsPostSchema(parser.SchemaByRequestParser):
    arguments = (reqparse.Argument("name", required=True, type=str),)
