import uuid
import sqlalchemy
from sqlalchemy.dialects import postgresql

import extensions
from app.model import enums
from app.model import utils
from app.model import fk_names

PERCH_MOUNT_NAME_MAX_LENGTH = 15


class PerchMounts(extensions.db.Model, utils.JsonAbleModel):
    __tablename__ = "perch_mounts"
    id = sqlalchemy.Column(
        postgresql.UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    perch_mount_name = sqlalchemy.Column(
        sqlalchemy.String(PERCH_MOUNT_NAME_MAX_LENGTH),
        unique=True,
        nullable=False,
    )
    longitude = sqlalchemy.Column(sqlalchemy.Float, nullable=False)
    latitude = sqlalchemy.Column(sqlalchemy.Float, nullable=False)
    habitat = sqlalchemy.Column(sqlalchemy.Enum(enums.Habitats), nullable=False)
    project_id = sqlalchemy.Column(
        postgresql.UUID(as_uuid=True),
        sqlalchemy.ForeignKey(fk_names.PROJECTS_ID),
        nullable=False,
    )
    claim_by_id = sqlalchemy.Column(
        postgresql.UUID(as_uuid=True),
        sqlalchemy.ForeignKey(fk_names.MEMBERS_ID),
    )
    mount_layer = sqlalchemy.Column(sqlalchemy.Enum(enums.MountLayers), nullable=False)
    terminated = sqlalchemy.Column(sqlalchemy.Boolean, default=False, nullable=False)
    is_priority = sqlalchemy.Column(sqlalchemy.Boolean, default=False, nullable=False)
    note = sqlalchemy.Column(sqlalchemy.Text)
