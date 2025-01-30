import uuid
import sqlalchemy
from sqlalchemy.dialects import postgresql

import app.extensions as extensions
from app.model import utils


class ColumnSize:
    PROJECT_NAME = 15
    MODEL_NAME = 30
    EVENT_NAME = 15
    BEHAVIOR_NAME = 15
    MOUNT_TYPE_NAME = 15


class Projects(extensions.db.Model, utils.JsonAbleModel):
    __tablename__ = "projects"
    id = extensions.db.Column(
        postgresql.UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    name = extensions.db.Column(
        sqlalchemy.String(ColumnSize.PROJECT_NAME),
        nullable=False,
        unique=True,
    )


class Cameras(extensions.db.Model, utils.JsonAbleModel):
    __tablename__ = "cameras"
    id = extensions.db.Column(
        postgresql.UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    model_name = extensions.db.Column(
        sqlalchemy.String(ColumnSize.MODEL_NAME),
        nullable=False,
        unique=True,
    )


class Events(extensions.db.Model, utils.JsonAbleModel):
    __tablename__ = "events"
    id = extensions.db.Column(
        postgresql.UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    name = extensions.db.Column(
        sqlalchemy.String(ColumnSize.EVENT_NAME),
        nullable=False,
        unique=True,
    )


class MountTypes(extensions.db.Model, utils.JsonAbleModel):
    __tablename__ = "mount_types"
    id = extensions.db.Column(
        postgresql.UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    name = extensions.db.Column(
        sqlalchemy.String(ColumnSize.MOUNT_TYPE_NAME),
        nullable=False,
        unique=True,
    )


class Behaviors(extensions.db.Model, utils.JsonAbleModel):
    __tablename__ = "behaviors"
    id = extensions.db.Column(
        postgresql.UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    name = extensions.db.Column(
        sqlalchemy.String(ColumnSize.BEHAVIOR_NAME),
        nullable=False,
        unique=True,
    )
