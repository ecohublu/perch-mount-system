import uuid
import sqlalchemy
from sqlalchemy.dialects import postgresql

import extensions
from app.model import enums
from app.model import utils
from app.model import fk_names


class Media(extensions.db.Model, utils.JsonAbleModel):
    __tablename__ = "media"
    id = sqlalchemy.Column(
        postgresql.UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    section_id = sqlalchemy.Column(
        postgresql.UUID(as_uuid=True),
        sqlalchemy.ForeignKey(fk_names.SECTIONS_ID),
        nullable=False,
    )
    medium_datetime = sqlalchemy.Column(sqlalchemy.DateTime)
    created_at = sqlalchemy.Column(
        sqlalchemy.DateTime,
        default=sqlalchemy.sql.func.now(),
        nullable=False,
    )
    medium_type = sqlalchemy.Column(sqlalchemy.Enum(enums.MediaType))
    nas_path = sqlalchemy.Column(sqlalchemy.String(255))
    # status create by migration sql.


class UndetectedMediaContents(extensions.db.Model, utils.JsonAbleModel):
    __tablename__ = "undetected_media_contents"
    medium_id = sqlalchemy.Column(
        postgresql.UUID(as_uuid=True),
        sqlalchemy.ForeignKey(fk_names.MEDIA_ID),
        nullable=False,
    )


class DetectedMediaContents(extensions.db.Model, utils.JsonAbleModel):
    __tablename__ = "detected_media_contents"
    medium_id = sqlalchemy.Column(
        postgresql.UUID(as_uuid=True),
        sqlalchemy.ForeignKey(fk_names.MEDIA_ID),
        nullable=False,
    )
    detected_at = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False)


class CheckedMediaContents(extensions.db.Model, utils.JsonAbleModel):
    __tablename__ = "checked_media_contents"
    medium_id = sqlalchemy.Column(
        postgresql.UUID(as_uuid=True),
        sqlalchemy.ForeignKey(fk_names.MEDIA_ID),
        nullable=False,
    )

    empty_checked_at = sqlalchemy.Column(sqlalchemy.DateTime)
    empty_checker_id = sqlalchemy.Column(
        postgresql.UUID(as_uuid=True),
        sqlalchemy.ForeignKey(fk_names.MEMBERS_ID),
        nullable=False,
    )


class UncheckedMediaContents(extensions.db.Model, utils.JsonAbleModel):
    __tablename__ = "unchecked_media_contents"
    medium_id = sqlalchemy.Column(
        postgresql.UUID(as_uuid=True),
        sqlalchemy.ForeignKey(fk_names.MEDIA_ID),
        nullable=False,
    )


class UnreviewedMediaContents(extensions.db.Model, utils.JsonAbleModel):
    __tablename__ = "unreviewed_media_contents"
    medium_id = sqlalchemy.Column(
        postgresql.UUID(as_uuid=True),
        sqlalchemy.ForeignKey(fk_names.MEDIA_ID),
        nullable=False,
    )


class ReviewedMediaContents(extensions.db.Model, utils.JsonAbleModel):
    __tablename__ = "reviewed_media_contents"
    medium_id = sqlalchemy.Column(
        postgresql.UUID(as_uuid=True),
        sqlalchemy.ForeignKey(fk_names.MEDIA_ID),
        nullable=False,
    )
    reviewed_at = sqlalchemy.Column(
        sqlalchemy.DateTime,
        default=sqlalchemy.sql.func.now(),
        nullable=False,
    )
    reviewer_id = sqlalchemy.Column(
        postgresql.UUID(as_uuid=True),
        sqlalchemy.ForeignKey(fk_names.MEMBERS_ID),
        nullable=False,
    )
    fearured_by_id = sqlalchemy.Column(
        postgresql.UUID(as_uuid=True),
        sqlalchemy.ForeignKey(fk_names.MEMBERS_ID),
    )
    event_id = sqlalchemy.Column(
        postgresql.UUID(as_uuid=True),
        sqlalchemy.ForeignKey(fk_names.EVENTS_ID),
    )
    behavior_id = sqlalchemy.Column(
        postgresql.UUID(as_uuid=True),
        sqlalchemy.ForeignKey(fk_names.BEHAVIORS_ID),
    )
