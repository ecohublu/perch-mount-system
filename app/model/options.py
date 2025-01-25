import uuid
import sqlalchemy
from sqlalchemy.dialects import postgresql

import extensions
from app.model import enums
from app.model import utils
from app.model import fk_names


PROJECT_NAME_MAX_LENGTH = 15
MODEL_NAME_MAX_LENGTH = 30
EVENT_NAME_MAX_LENGTH = 15
MOUNT_TYPE_NAME_MAX_LENGTH = 15


class Projects(extensions.db.Model, utils.JsonAbleModel):
    __tablename__ = "projects"
    id = sqlalchemy.Column(
        postgresql.UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    name = sqlalchemy.Column(sqlalchemy.String(PROJECT_NAME_MAX_LENGTH))


class Cameras(extensions.db.Model, utils.JsonAbleModel):
    __tablename__ = "cameras"
    id = sqlalchemy.Column(
        postgresql.UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    model_name = sqlalchemy.Column(sqlalchemy.String(MODEL_NAME_MAX_LENGTH))


class Events(extensions.db.Model, utils.JsonAbleModel):
    __tablename__ = "events"
    id = sqlalchemy.Column(
        postgresql.UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    name = sqlalchemy.Column(sqlalchemy.String(EVENT_NAME_MAX_LENGTH))


class MountTypes(extensions.db.Model, utils.JsonAbleModel):
    __tablename__ = "mount_types"
    id = sqlalchemy.Column(
        postgresql.UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    name = sqlalchemy.Column(sqlalchemy.String(MOUNT_TYPE_NAME_MAX_LENGTH))
