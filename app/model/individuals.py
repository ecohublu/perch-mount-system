import uuid
import sqlalchemy
from sqlalchemy.dialects import postgresql
import sqlalchemy.orm

import app.extensions as extensions
from app.model import enums
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
        sqlalchemy.ForeignKey(fk_names.MEDIA_ID),
        nullable=False,
    )
    note = extensions.db.Column(sqlalchemy.Text)
    prey_status = extensions.db.Column(
        sqlalchemy.Enum(enums.MediaStatus),
        default="UNCHECKED",
        server_default="UNCHECKED",
    )

    medium = sqlalchemy.orm.relationship("Media", lazy="subquery")

    unreviewed_contents = sqlalchemy.orm.relationship("UnreviewedIndividualsContents")
    reviewed_contents = sqlalchemy.orm.relationship("ReviewedIndividualsContents")
    marked_prey_contents = sqlalchemy.orm.relationship("MarkedPreyIndividualsContents")
    identified_prey_contents = sqlalchemy.orm.relationship("IdentifiedPreyIndividualsContents")
    tagged_contents = sqlalchemy.orm.relationship("TaggedIndividualsContents")


class UnreviewedIndividualsContents(extensions.db.Model, utils.JsonAbleModel):
    __tablename__ = "unreviewed_individuals_contents"
    individual_id = extensions.db.Column(
        postgresql.UUID(as_uuid=True),
        sqlalchemy.ForeignKey(fk_names.INDIVIDUALS_ID),
        nullable=False,
        primary_key=True,
    )
    taxon_order_by_ai = extensions.db.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey(fk_names.SPECIES_TAXON_ORDER),
        nullable=False,
    )
    box_xmin = extensions.db.Column(sqlalchemy.Float)
    box_xmax = extensions.db.Column(sqlalchemy.Float)
    box_ymin = extensions.db.Column(sqlalchemy.Float)
    box_ymax = extensions.db.Column(sqlalchemy.Float)

    __table_arg__ = sqlalchemy.CheckConstraint(
        "box_xmin >= 0 AND box_xmin <= 1",
        "box_xmax >= 0 AND box_xmax <= 1",
        "box_ymin >= 0 AND box_ymin <= 1",
        "box_ymax >= 0 AND box_ymax <= 1",
    )


class ReviewedIndividualsContents(extensions.db.Model, utils.JsonAbleModel):
    __tablename__ = "reviewed_individuals_contents"
    individual_id = extensions.db.Column(
        postgresql.UUID(as_uuid=True),
        sqlalchemy.ForeignKey(fk_names.INDIVIDUALS_ID),
        nullable=False,
        primary_key=True,
    )
    taxon_order_by_human = extensions.db.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey(fk_names.SPECIES_TAXON_ORDER),
        nullable=False,
    )
    box_xmin = extensions.db.Column(sqlalchemy.Float)
    box_xmax = extensions.db.Column(sqlalchemy.Float)
    box_ymin = extensions.db.Column(sqlalchemy.Float)
    box_ymax = extensions.db.Column(sqlalchemy.Float)

    __table_arg__ = sqlalchemy.CheckConstraint(
        "box_xmin >= 0 AND box_xmin <= 1",
        "box_xmax >= 0 AND box_xmax <= 1",
        "box_ymin >= 0 AND box_ymin <= 1",
        "box_ymax >= 0 AND box_ymax <= 1",
    )


class MarkedPreyIndividualsContents(extensions.db.Model, utils.JsonAbleModel):
    __tablename__ = "marded_prey_individuals_contents"
    individual_id = extensions.db.Column(
        postgresql.UUID(as_uuid=True),
        sqlalchemy.ForeignKey(fk_names.INDIVIDUALS_ID),
        nullable=False,
        primary_key=True,
    )
    has_prey = extensions.db.Column(sqlalchemy.Boolean, nullable=False)


class IdentifiedPreyIndividualsContents(extensions.db.Model, utils.JsonAbleModel):
    __tablename__ = "identified_prey_individuals_contents"
    individual_id = extensions.db.Column(
        postgresql.UUID(as_uuid=True),
        sqlalchemy.ForeignKey(fk_names.INDIVIDUALS_ID),
        nullable=False,
        primary_key=True,
    )
    inaturalist_taxa_id = extensions.db.Column(sqlalchemy.Integer, nullable=False)
    identifier_id = extensions.db.Column(
        postgresql.UUID(as_uuid=True),
        sqlalchemy.ForeignKey(fk_names.MEMBERS_ID),
        nullable=False,
    )


class TaggedIndividualsContents(extensions.db.Model, utils.JsonAbleModel):
    __tablename__ = "tagged_individuals_contents"
    individual_id = extensions.db.Column(
        postgresql.UUID(as_uuid=True),
        sqlalchemy.ForeignKey(fk_names.INDIVIDUALS_ID),
        nullable=False,
        primary_key=True,
    )
    is_tagged = extensions.db.Column(sqlalchemy.Boolean, nullable=False)
    has_ring = extensions.db.Column(sqlalchemy.Boolean, nullable=False)
    ring_number = extensions.db.Column(sqlalchemy.String(20))
