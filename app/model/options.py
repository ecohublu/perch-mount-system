import uuid
import sqlalchemy
from sqlalchemy.dialects import postgresql

import extensions
from app.model import utils


class ColumnSize:
    PROJECT_NAME = 15
    MODEL_NAME = 30
    EVENT_NAME = 15
    MOUNT_TYPE_NAME = 15


class Projects(extensions.db.Model, utils.JsonAbleModel):
    __tablename__ = "projects"
    id = sqlalchemy.Column(
        postgresql.UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    name = sqlalchemy.Column(sqlalchemy.String(ColumnSize.PROJECT_NAME))


class Cameras(extensions.db.Model, utils.JsonAbleModel):
    __tablename__ = "cameras"
    id = sqlalchemy.Column(
        postgresql.UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    model_name = sqlalchemy.Column(sqlalchemy.String(ColumnSize.MODEL_NAME))


class Events(extensions.db.Model, utils.JsonAbleModel):
    __tablename__ = "events"
    id = sqlalchemy.Column(
        postgresql.UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    name = sqlalchemy.Column(sqlalchemy.String(ColumnSize.EVENT_NAME))


class MountTypes(extensions.db.Model, utils.JsonAbleModel):
    __tablename__ = "mount_types"
    id = sqlalchemy.Column(
        postgresql.UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    name = sqlalchemy.Column(sqlalchemy.String(ColumnSize.MOUNT_TYPE_NAME))
