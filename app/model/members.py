import uuid
import re
import sqlalchemy
from sqlalchemy.dialects import postgresql


import extensions
from app.model import enums
from app.model import utils


USER_NAME_MAX_LENGTH = 50
FIRST_NAME_MAX_LENGTH = 50
LAST_NAME_MAX_LENGTH = 50


class Members(extensions.db.Model, utils.JsonAbleModel):
    __tablename__ = "members"
    id = sqlalchemy.Column(
        postgresql.UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    gmail = sqlalchemy.Column(postgresql.CITEXT, nullable=False, unique=True)
    user_name = sqlalchemy.Column(
        sqlalchemy.String(USER_NAME_MAX_LENGTH),
        unique=True,
        nullable=False,
    )
    first_name = sqlalchemy.Column(
        sqlalchemy.String(FIRST_NAME_MAX_LENGTH),
        nullable=False,
    )
    last_name = sqlalchemy.Column(
        sqlalchemy.String(LAST_NAME_MAX_LENGTH),
        nullable=False,
    )
    position = sqlalchemy.Column(
        sqlalchemy.Enum(enums.Positions),
        nullable=False,
    )
    is_admin = sqlalchemy.Column(
        sqlalchemy.Boolean,
        default=False,
        nullable=False,
    )
    is_super_admin = sqlalchemy.Column(
        sqlalchemy.Boolean,
        default=False,
        nullable=False,
    )
    blocked = sqlalchemy.Column(
        sqlalchemy.Boolean,
        default=False,
        nullable=False,
    )
    activated = sqlalchemy.Column(
        sqlalchemy.Boolean,
        default=False,
        nullable=False,
    )

    @sqlalchemy.orm.validates("gamil")
    def validate_email(self, key, email):

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid email address")
        return email
