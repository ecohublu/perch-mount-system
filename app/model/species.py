import sqlalchemy
from sqlalchemy.dialects import postgresql

import app.extensions as extensions
from app.model import enums
from app.model import utils


class ColumnSizes:
    SCIENTIFIC_NAME = 100
    ENGLISH_COMMON_NAME = 100
    CHINESE_COMMON_NAME = 50
    CATEGORY = 15
    ORDER = 50
    FAMILY_NAME = 50
    FAMILY_LATIN_NAME = 50
    TAIWAN_STATUS = 50
    MATZU_STATUS = 50
    KINMEN_STATUS = 50
    PRATAS_STATUS = 50
    ENDEMISM = 50
    CODES = 10


class Species(extensions.db.Model, utils.JsonAbleModel):
    __tablename__ = "species"
    taxon_order = extensions.db.Column(
        sqlalchemy.Integer,
        primary_key=True,
        nullable=False,
        unique=True,
    )
    scientific_name = extensions.db.Column(
        sqlalchemy.String(ColumnSizes.SCIENTIFIC_NAME),
        nullable=False,
        unique=True,
    )
    english_common_name = extensions.db.Column(
        sqlalchemy.String(ColumnSizes.ENGLISH_COMMON_NAME),
        nullable=False,
        unique=True,
    )
    chinese_common_name = extensions.db.Column(
        sqlalchemy.String(ColumnSizes.CHINESE_COMMON_NAME),
        nullable=False,
        unique=True,
    )
    category = extensions.db.Column(sqlalchemy.String(ColumnSizes.CATEGORY))
    order = extensions.db.Column(
        sqlalchemy.String(ColumnSizes.ORDER),
        nullable=False,
    )
    family_name = extensions.db.Column(
        sqlalchemy.String(ColumnSizes.FAMILY_NAME),
        nullable=False,
    )
    family_latin_name = extensions.db.Column(
        sqlalchemy.String(ColumnSizes.FAMILY_LATIN_NAME),
        nullable=False,
    )
    taiwan_status = extensions.db.Column(sqlalchemy.String(ColumnSizes.TAIWAN_STATUS))
    matzu_status = extensions.db.Column(sqlalchemy.String(ColumnSizes.MATZU_STATUS))
    kinmen_status = extensions.db.Column(sqlalchemy.String(ColumnSizes.KINMEN_STATUS))
    pratas_status = extensions.db.Column(sqlalchemy.String(ColumnSizes.PRATAS_STATUS))
    endemism = extensions.db.Column(sqlalchemy.String(ColumnSizes.ENDEMISM))
    conservation_status = extensions.db.Column(
        sqlalchemy.Enum(enums.ConservationStatus)
    )
    codes = extensions.db.Column(postgresql.ARRAY(sqlalchemy.String(ColumnSizes.CODES)))
