import marshmallow


class SectionPatchSchema(marshmallow.Schema):
    mount_type_id = marshmallow.fields.uuid()
    camera_id = marshmallow.fields.uuid()
    note = marshmallow.fields.String()


class PerchMountPatchSchema(marshmallow.Schema):
    longitude = marshmallow.fields.uuid()
    latitude = marshmallow.fields.uuid()
    habitat = marshmallow.fields.String()
    claim_by_id = marshmallow.fields.uuid()
    mount_layer = marshmallow.fields.String()
    terminated = marshmallow.fields.String()
    is_priority = marshmallow.fields.Boolean()
    note = marshmallow.fields.String()


class MemberPatchSchema(marshmallow.Schema):
    first_name = marshmallow.fields.String()
    last_name = marshmallow.fields.String()
    position = marshmallow.fields.String()


class MediaPatchSchema(marshmallow.Schema):
    fearured_by_id = marshmallow.fields.uuid()
    behavior_id = marshmallow.fields.uuid()
    event_id = marshmallow.fields.uuid()


class IndividualPatchSchema(marshmallow.Schema):
    note = marshmallow.fields.String()
    taxon_order_by_human = marshmallow.fields.Integer()
    box_xmin = marshmallow.fields.Float()
    box_xmax = marshmallow.fields.Float()
    box_ymin = marshmallow.fields.Float()
    box_ymax = marshmallow.fields.Float()
    has_prey = marshmallow.fields.Boolean()
    inaturalist_taxa_id = marshmallow.fields.Integer()
    identifier_id = marshmallow.fields.Integer()
    is_tagged = marshmallow.fields.Boolean()
    has_ring = marshmallow.fields.Boolean()
    ring_number = marshmallow.fields.String()
