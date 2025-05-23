from datetime import datetime
from flask_restx import reqparse
import uuid

from app.resources.utils import parser
from app.resources.utils import type_funcs


class FeaturesGetSchema(parser.SchemaByRequestParser):

    arguments = (
        # 1. 時間範圍
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
        # 2. 多選 UUID 陣列
        reqparse.Argument(
            "behavior_ids",
            type=type_funcs.uuid_split,
            location="args",
        ),
        reqparse.Argument(
            "project_ids",
            type=type_funcs.uuid_split,
            location="args",
        ),
        reqparse.Argument(
            "perch_mount_ids",
            type=type_funcs.uuid_split,
            location="args",
        ),
        reqparse.Argument(
            "taxon_orders",
            type=type_funcs.int_split,
            location="arg",
        ),
        # 3. 單一 UUID
        reqparse.Argument(
            "featured_by_id",
            type=uuid.UUID,
            location="args",
        ),
        reqparse.Argument(
            "offset",
            type=int,
            default=0,
            location="args",
        ),
        reqparse.Argument(
            "limit",
            type=int,
            default=50,
            location="args",
        ),
    )


class Features(parser.Parser):
    get = FeaturesGetSchema()
