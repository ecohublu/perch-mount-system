import uuid
import sqlalchemy
from sqlalchemy.dialects import postgresql

import app.extensions as extensions
from app.model import enums
from app.model import utils
from app.model import fk_names


class Media(extensions.db.Model, utils.JsonAbleModel):
    __tablename__ = "media"
    id = extensions.db.Column(
        postgresql.UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    section_id = extensions.db.Column(
        postgresql.UUID(as_uuid=True),
        sqlalchemy.ForeignKey(fk_names.SECTIONS_ID),
        nullable=False,
    )
    medium_datetime = extensions.db.Column(sqlalchemy.DateTime)
    created_at = extensions.db.Column(
        sqlalchemy.DateTime,
        default=sqlalchemy.sql.func.now(),
        nullable=False,
    )
    medium_type = extensions.db.Column(sqlalchemy.Enum(enums.MediaType), nullable=False)
    nas_path = extensions.db.Column(sqlalchemy.String(255))
    # status implmeneted in migrations. It recorded in the view table: media_status


class UndetectedMediaContents(extensions.db.Model, utils.JsonAbleModel):
    __tablename__ = "undetected_media_contents"
    medium_id = extensions.db.Column(
        postgresql.UUID(as_uuid=True),
        sqlalchemy.ForeignKey(fk_names.MEDIA_ID),
        nullable=False,
    )


class MediaDetectedContents(extensions.db.Model, utils.JsonAbleModel):
    __tablename__ = "media_detected_contents"
    medium_id = extensions.db.Column(
        postgresql.UUID(as_uuid=True),
        sqlalchemy.ForeignKey(fk_names.MEDIA_ID),
        nullable=False,
    )
    detected_at = extensions.db.Column(sqlalchemy.DateTime)


class MediaCheckedontents(extensions.db.Model, utils.JsonAbleModel):
    __tablename__ = "media_checked_contents"
    medium_id = extensions.db.Column(
        postgresql.UUID(as_uuid=True),
        sqlalchemy.ForeignKey(fk_names.MEDIA_ID),
        nullable=False,
    )

    empty_checked_at = extensions.db.Column(sqlalchemy.DateTime)
    empty_checker_id = extensions.db.Column(
        postgresql.UUID(as_uuid=True),
        sqlalchemy.ForeignKey(fk_names.MEMBERS_ID),
    )


class UncheckedMediaContents(extensions.db.Model, utils.JsonAbleModel):
    __tablename__ = "unchecked_media_contents"
    medium_id = extensions.db.Column(
        postgresql.UUID(as_uuid=True),
        sqlalchemy.ForeignKey(fk_names.MEDIA_ID),
        nullable=False,
    )


class UnreviewedMediaContents(extensions.db.Model, utils.JsonAbleModel):
    __tablename__ = "unreviewed_media_contents"
    medium_id = extensions.db.Column(
        postgresql.UUID(as_uuid=True),
        sqlalchemy.ForeignKey(fk_names.MEDIA_ID),
        nullable=False,
    )


class ReviewedMediaContents(extensions.db.Model, utils.JsonAbleModel):
    __tablename__ = "reviewed_media_contents"
    medium_id = extensions.db.Column(
        postgresql.UUID(as_uuid=True),
        sqlalchemy.ForeignKey(fk_names.MEDIA_ID),
        nullable=False,
    )
    reviewed_at = extensions.db.Column(
        sqlalchemy.DateTime,
        default=sqlalchemy.sql.func.now(),
        nullable=False,
    )
    reviewer_id = extensions.db.Column(
        postgresql.UUID(as_uuid=True),
        sqlalchemy.ForeignKey(fk_names.MEMBERS_ID),
        nullable=False,
    )
    fearured_by_id = extensions.db.Column(
        postgresql.UUID(as_uuid=True),
        sqlalchemy.ForeignKey(fk_names.MEMBERS_ID),
    )
    event_id = extensions.db.Column(
        postgresql.UUID(as_uuid=True),
        sqlalchemy.ForeignKey(fk_names.EVENTS_ID),
    )
    behavior_id = extensions.db.Column(
        postgresql.UUID(as_uuid=True),
        sqlalchemy.ForeignKey(fk_names.BEHAVIORS_ID),
    )
