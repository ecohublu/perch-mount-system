import uuid
import sqlalchemy
from sqlalchemy.dialects import postgresql

import app.extensions as extensions
from app.model import utils
from app.model import fk_names


class Individuals(extensions.db.Model, utils.JsonAbleModel):
    __tablename__ = "individuals"
    id = extensions.db.Column(
        postgresql.UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    medium_id = extensions.db.Column(
        postgresql.UUID(as_uuid=True),
        sqlalchemy.ForeignKey(fk_names.INDIVIDUALS_ID),
        nullable=False,
    )
    note = extensions.db.Column(sqlalchemy.Text)
    # prey_identified_status and tag_status will be defined in the migration file.


class UnreviewedIndividualsContents(extensions.db.Model, utils.JsonAbleModel):
    __table__ = "unreviewed_individuals_contents"
    individual_id = extensions.db.Column(
        postgresql.UUID(as_uuid=True),
        sqlalchemy.ForeignKey(fk_names.INDIVIDUALS_ID),
        nullable=False,
    )
    taxon_order_by_ai = extensions.db.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey(fk_names.SPECIES_TAXON_ORDER),
        nullable=False,
    )
    xmin = extensions.db.Column(sqlalchemy.Float)
    xmax = extensions.db.Column(sqlalchemy.Float)
    ymin = extensions.db.Column(sqlalchemy.Float)
    ymax = extensions.db.Column(sqlalchemy.Float)

    __table_arg__ = sqlalchemy.CheckConstraint(
        "xmin >= 0 AND xmin <= 1",
        "xmax >= 0 AND xmax <= 1",
        "ymin >= 0 AND ymin <= 1",
        "ymax >= 0 AND ymax <= 1",
    )


class ReviewedIndividualsContents(extensions.db.Model, utils.JsonAbleModel):
    __table__ = "reviewed_individuals_contents"
    individual_id = extensions.db.Column(
        postgresql.UUID(as_uuid=True),
        sqlalchemy.ForeignKey(fk_names.INDIVIDUALS_ID),
        nullable=False,
    )
    taxon_order_by_human = extensions.db.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey(fk_names.SPECIES_TAXON_ORDER)
    )
    xmin = extensions.db.Column(sqlalchemy.Float)
    xmax = extensions.db.Column(sqlalchemy.Float)
    ymin = extensions.db.Column(sqlalchemy.Float)
    ymax = extensions.db.Column(sqlalchemy.Float)

    __table_arg__ = sqlalchemy.CheckConstraint(
        "xmin >= 0 AND xmin <= 1",
        "xmax >= 0 AND xmax <= 1",
        "ymin >= 0 AND ymin <= 1",
        "ymax >= 0 AND ymax <= 1",
    )


class MarkedPreyIndividualsContents(extensions.db.Model, utils.JsonAbleModel):
    __table__ = "marded_prey_individuals_contents"
    individual_id = extensions.db.Column(
        postgresql.UUID(as_uuid=True),
        sqlalchemy.ForeignKey(fk_names.INDIVIDUALS_ID),
        nullable=False,
    )
    has_prey = extensions.db.Column(sqlalchemy.Boolean, nullable=False)


class IdentifiedPreyIndividualsContents(extensions.db.Model, utils.JsonAbleModel):
    __table__ = "identified_prey_individuals_contents"
    individual_id = extensions.db.Column(
        postgresql.UUID(as_uuid=True),
        sqlalchemy.ForeignKey(fk_names.INDIVIDUALS_ID),
        nullable=False,
    )
    inaturalist_taxa_id = extensions.db.Column(sqlalchemy.Integer, nullable=False)
    identifier_id = extensions.db.Column(
        postgresql.UUID(as_uuid=True),
        sqlalchemy.ForeignKey(fk_names.MEMBERS_ID),
        nullable=False,
    )


class TaggedIndividualsContents(extensions.db.Model, utils.JsonAbleModel):
    __table__ = "Tagged_individuals_contents"
    individual_id = extensions.db.Column(
        postgresql.UUID(as_uuid=True),
        sqlalchemy.ForeignKey(fk_names.INDIVIDUALS_ID),
        nullable=False,
    )
    is_tagged = extensions.db.Column(sqlalchemy.Boolean, nullable=False)
    has_ring = extensions.db.Column(sqlalchemy.Boolean, nullable=False)
    ring_number = extensions.db.Column(sqlalchemy.String(20))
