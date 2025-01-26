import uuid
import sqlalchemy
from sqlalchemy.dialects import postgresql

import app.extensions as extensions
from app.model import utils
from app.model import fk_names


class Sections(extensions.db.Model, utils.JsonAbleModel):
    __tablename__ = "sections"
    id = extensions.db.Column(
        postgresql.UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    perch_mount_id = extensions.db.Column(
        postgresql.UUID(as_uuid=True),
        sqlalchemy.ForeignKey(fk_names.PERCH_MOUNTS_ID),
        nullable=False,
    )
    mount_type_id = extensions.db.Column(
        postgresql.UUID(as_uuid=True),
        sqlalchemy.ForeignKey(fk_names.MOUNT_TYPES_ID),
        nullable=False,
    )
    camera_id = extensions.db.Column(
        postgresql.UUID(as_uuid=True),
        sqlalchemy.ForeignKey(fk_names.CAMERAS_ID),
        nullable=False,
    )
    swapped_date = extensions.db.Column(
        sqlalchemy.Date,
        nullable=False,
    )
    valid = extensions.db.Column(
        sqlalchemy.Boolean,
        default=True,
        nullable=False,
    )
    note = extensions.db.Column(sqlalchemy.Text)


class SectionSwappers(extensions.db.Model, utils.JsonAbleModel):
    __tablename__ = "section_swappers"
    section_id = extensions.db.Column(
        postgresql.UUID(as_uuid=True),
        sqlalchemy.ForeignKey(fk_names.SECTIONS_ID),
        primary_key=True,
        nullable=False,
    )
    swapper_id = extensions.db.Column(
        postgresql.UUID(as_uuid=True),
        sqlalchemy.ForeignKey(fk_names.MEMBERS_ID),
        primary_key=True,
        nullable=False,
    )
