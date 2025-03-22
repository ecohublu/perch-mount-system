import marshmallow
import marshmallow.schema


class SectionPatchSchema(marshmallow.Schema):
    mount_type_id = marshmallow.fields.UUID()
    camera_id = marshmallow.fields.UUID()
    note = marshmallow.fields.String()


class PerchMountPatchSchema(marshmallow.Schema):
    longitude = marshmallow.fields.UUID()
    latitude = marshmallow.fields.UUID()
    habitat = marshmallow.fields.String()
    claim_by_id = marshmallow.fields.UUID()
    mount_layer = marshmallow.fields.String()
    terminated = marshmallow.fields.String()
    is_priority = marshmallow.fields.Boolean()
    note = marshmallow.fields.String()


class MemberPatchSchema(marshmallow.Schema):
    first_name = marshmallow.fields.String()
    last_name = marshmallow.fields.String()
    position = marshmallow.fields.String()


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


class IndividualTagPatchSchema(marshmallow.Schema):
    is_tagged = marshmallow.fields.Boolean()
    has_ring = marshmallow.fields.Boolean()
    ring_number = marshmallow.fields.String()
