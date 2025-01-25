import uuid
import sqlalchemy
from sqlalchemy.dialects import postgresql

import extensions
from app.model import utils
from app.model import fk_names


class Sections(extensions.db.Model, utils.JsonAbleModel):
    __tablename__ = "sections"
    id = sqlalchemy.Column(
        postgresql.UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    perch_mount_id = sqlalchemy.Column(
        postgresql.UUID(as_uuid=True),
        sqlalchemy.ForeignKey(fk_names.PERCH_MOUNTS_ID),
        nullable=False,
    )
    mount_type_id = sqlalchemy.Column(
        postgresql.UUID(as_uuid=True),
        sqlalchemy.ForeignKey(fk_names.MOUNT_TYPES_ID),
        nullable=False,
    )
    camera_id = sqlalchemy.Column(
        postgresql.UUID(as_uuid=True),
        sqlalchemy.ForeignKey(fk_names.CAMERAS_ID),
        nullable=False,
    )
    swapped_date = sqlalchemy.Column(
        sqlalchemy.Date,
        nullable=False,
    )
    valid = sqlalchemy.Column(
        sqlalchemy.Boolean,
        default=True,
        nullable=False,
    )
    note = sqlalchemy.Column(sqlalchemy.Text)


class SectionSwappers(extensions.db.Model, utils.JsonAbleModel):
    __tablename__ = "section_swappers"
    section_id = sqlalchemy.Column(
        postgresql.UUID(as_uuid=True),
        sqlalchemy.ForeignKey(fk_names.SECTIONS_ID),
        primary_key=True,
        nullable=False,
    )
    swapper_id = sqlalchemy.Column(
        postgresql.UUID(as_uuid=True),
        sqlalchemy.ForeignKey(fk_names.MEMBERS_ID),
        primary_key=True,
        nullable=False,
    )
