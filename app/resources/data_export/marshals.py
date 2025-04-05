from flask_restx import fields

data_model = {
    # _DEFAULT_FIELDS
    "project": fields.String,
    "perch_mount_name": fields.String,
    "swapped_date": fields.Date,
    "medium_datetime": fields.DateTime,
    "chinese_common_name_by_ai": fields.String,
    "chinese_common_name_by_human": fields.String,
    # perch_mount
    "longitude": fields.Float,
    "latitude": fields.Float,
    "habitat": fields.String,
    "mount_layer": fields.String,
    # section
    "mount_type": fields.String,
    "camera": fields.String,
    "start_time": fields.DateTime,
    "end_time": fields.DateTime,
    # species
    "taxon_order_by_ai": fields.Integer,
    "taxon_order_by_human": fields.Integer,
    "english_common_name_by_ai": fields.String,
    "english_common_name_by_human": fields.String,
    "scientific_name_by_ai": fields.String,
    "scientific_name_by_human": fields.String,
    # prey
    "has_prey": fields.String,
    "prey_inat_id": fields.Integer,
    # tag
    "is_tagged": fields.Boolean,
    "has_ring": fields.Boolean,
    "ring_number": fields.String,
    # yolo
    "unreviewed_xmax": fields.Float,
    "unreviewed_xmin": fields.Float,
    "unreviewed_ymax": fields.Float,
    "unreviewed_ymin": fields.Float,
    "reviewed_xmax": fields.Float,
    "reviewed_xmin": fields.Float,
    "reviewed_ymax": fields.Float,
    "reviewed_ymin": fields.Float,
}
