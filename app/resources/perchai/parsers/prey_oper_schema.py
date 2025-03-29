import marshmallow


class IdentifiedPreySchema(marshmallow.Schema):
    individual_id = marshmallow.fields.UUID()
    inaturalist_taxa_id = marshmallow.fields.Integer()
    identifier_id = marshmallow.fields.UUID()
