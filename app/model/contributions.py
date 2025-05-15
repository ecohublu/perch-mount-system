import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.dialects import postgresql
import uuid

import app.extensions as extensions
from app.model import enums
from app.model import fk_names


class Contributions(extensions.db.Model, SerializerMixin):
    id = extensions.db.Column(
        postgresql.UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    contribution_type = extensions.db.Column(
        sqlalchemy.Enum(enums.ContributionType),
        nullable=False,
    )
    counts = extensions.db.Column(
        sqlalchemy.Integer,
        nullable=False,
    )
    contributor_id = extensions.db.Column(
        postgresql.UUID(as_uuid=True),
        sqlalchemy.ForeignKey(fk_names.MEMBERS_ID),
        nullable=False,
    )
    contribute_time = extensions.db.Column(
        sqlalchemy.DateTime,
        default=sqlalchemy.sql.func.now(),
        server_default=sqlalchemy.func.now(),
        nullable=False,
    )
