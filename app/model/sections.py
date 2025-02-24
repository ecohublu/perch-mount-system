import uuid
import sqlalchemy
from sqlalchemy.dialects import postgresql
import sqlalchemy.orm
from sqlalchemy_serializer import SerializerMixin

from app import extensions
from app.model import fk_names


sections_swappers = sqlalchemy.Table(
    "sections_swappers",
    extensions.db.metadata,
    sqlalchemy.Column(
        "section_id",
        postgresql.UUID(as_uuid=True),
        sqlalchemy.ForeignKey("sections.id"),
        primary_key=True,
    ),
    sqlalchemy.Column(
        "swapper_id",
        postgresql.UUID(as_uuid=True),
        sqlalchemy.ForeignKey("members.id"),
        primary_key=True,
    ),
)


class Sections(extensions.db.Model, SerializerMixin):
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
    start_time = extensions.db.Column(sqlalchemy.DateTime)
    end_time = extensions.db.Column(sqlalchemy.DateTime)
    valid = extensions.db.Column(
        sqlalchemy.Boolean,
        default=True,
        server_default=sqlalchemy.text("FALSE"),
        nullable=False,
    )
    note = extensions.db.Column(sqlalchemy.Text)
    undetected_count = extensions.db.Column(sqlalchemy.Integer, default=0)
    unchecked_count = extensions.db.Column(sqlalchemy.Integer, default=0)
    unreviewed_count = extensions.db.Column(sqlalchemy.Integer, default=0)
    reviewed_count = extensions.db.Column(sqlalchemy.Integer, default=0)
    accidental_count = extensions.db.Column(sqlalchemy.Integer, default=0)

    camera = sqlalchemy.orm.relationship("Cameras", lazy="immediate")
    mount_type = sqlalchemy.orm.relationship("MountTypes", lazy="immediate")
    swappers = sqlalchemy.orm.relationship(
        "Members", secondary=sections_swappers, lazy="immediate"
    )
    __table_arg__ = sqlalchemy.CheckConstraint("start_time <= end_time")
