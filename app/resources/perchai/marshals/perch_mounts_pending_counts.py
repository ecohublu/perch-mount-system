from flask_restx import fields


COUNTS_MODEL = {
    "id": fields.String,
    "perch_mount_name": fields.String,
    "undetected_count": fields.Integer,
    "unchecked_count": fields.Integer,
    "unreviewed_count": fields.Integer,
    "reviewed_count": fields.Integer,
    "accidental_count": fields.Integer,
}
