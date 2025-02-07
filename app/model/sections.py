import uuid
import sqlalchemy
from sqlalchemy.dialects import postgresql
import sqlalchemy.orm

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
        server_default=sqlalchemy.text("FALSE"),
        nullable=False,
    )
    swapper_ids = extensions.db.Column(postgresql.ARRAY(postgresql.UUID(as_uuid=True)))
    note = extensions.db.Column(sqlalchemy.Text)

    perch_mount = sqlalchemy.orm.relationship("PerchMounts")
    swappers = sqlalchemy.orm.relationship("Members", lazy="subquery")
    camera = sqlalchemy.orm.relationship("Cameras", lazy="immediate")
    mount_type = sqlalchemy.orm.relationship("MountTypes", lazy="immediate")
