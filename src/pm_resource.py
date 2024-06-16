import datetime
import flask_restful


TRUES = {"true", "1", "yes", "y", "ya"}


def _query_bool(phase: str) -> bool:
    return phase.lower() in TRUES


def _string_to_int_list(arg: str) -> list[int]:
    if not arg:
        return []
    return [int(a) for a in arg.split(",")]


def _string_to_str_list(arg: str) -> list[int]:
    return arg.split(",")


TYPE_MAP = (
    ("section", int),
    ("perch_mount", int),
    ("offset", int),
    ("limit", int),
    ("section_id", int),
    ("perch_mount_id", int),
    ("taxon_order", int),
    ("category", str),
    ("order", str),
    ("family", str),
    ("prey", _query_bool),
    ("project", int),
    ("habitat", int),
    ("terminated", _query_bool),
    ("claim_by", int),
    ("perch_mount", int),
    ("check_date_from", datetime.datetime.fromisoformat),
    ("check_date_to", datetime.datetime.fromisoformat),
    ("new_start_time", datetime.datetime.fromisoformat),
    ("start_time", datetime.datetime.fromisoformat),
    ("end_time", datetime.datetime.fromisoformat),
    ("operator", int),
    ("project_ids", _string_to_int_list),
    ("perch_mount_ids", _string_to_int_list),
    ("section_ids", _string_to_int_list),
    ("prey_names", _string_to_str_list),
    ("taxon_orders_by_human", _string_to_int_list),
    ("taxon_orders_by_ai", _string_to_int_list),
    ("unreviewed_data", _query_bool),
    ("exportor", int),
    ("featured", _query_bool),
    ("featured_by", int),
    ("featured_behavior", int),
)


class PerchMountResource(flask_restful.Resource):
    def _correct_types(self, args: dict) -> dict:
        for colname, type in TYPE_MAP:
            if colname in args:
                args[colname] = type(args[colname])
        return args
