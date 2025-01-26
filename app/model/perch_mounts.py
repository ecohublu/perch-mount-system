import uuid
import sqlalchemy
from sqlalchemy.dialects import postgresql

import app.extensions as extensions
from app.model import enums
from app.model import utils
from app.model import fk_names


class ColumnSize:
    PERCH_MOUNT_NAME = 15


class PerchMounts(extensions.db.Model, utils.JsonAbleModel):
    __tablename__ = "perch_mounts"
    id = extensions.db.Column(
        postgresql.UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    perch_mount_name = extensions.db.Column(
        sqlalchemy.String(ColumnSize.PERCH_MOUNT_NAME),
        unique=True,
        nullable=False,
    )
    longitude = extensions.db.Column(sqlalchemy.Float, nullable=False)
    latitude = extensions.db.Column(sqlalchemy.Float, nullable=False)
    habitat = extensions.db.Column(sqlalchemy.Enum(enums.Habitats), nullable=False)
    project_id = extensions.db.Column(
        postgresql.UUID(as_uuid=True),
        sqlalchemy.ForeignKey(fk_names.PROJECTS_ID),
        nullable=False,
    )
    claim_by_id = extensions.db.Column(
        postgresql.UUID(as_uuid=True),
        sqlalchemy.ForeignKey(fk_names.MEMBERS_ID),
    )
    mount_layer = extensions.db.Column(
        sqlalchemy.Enum(enums.MountLayers), nullable=False
    )
    terminated = extensions.db.Column(sqlalchemy.Boolean, default=False, nullable=False)
    is_priority = extensions.db.Column(
        sqlalchemy.Boolean, default=False, nullable=False
    )
    note = extensions.db.Column(sqlalchemy.Text)
