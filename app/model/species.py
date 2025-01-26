import sqlalchemy
from sqlalchemy.dialects import postgresql

import extensions
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


class Species(extensions.db.Model, utils.JsonAbleModel):
    __tablename__ = "species"
    taxon_order = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    scientific_name = sqlalchemy.Column(sqlalchemy.String(ColumnSizes.SCIENTIFIC_NAME))
    english_common_name = sqlalchemy.Column(
        sqlalchemy.String(ColumnSizes.ENGLISH_COMMON_NAME)
    )
    chinese_common_name = sqlalchemy.Column(
        sqlalchemy.String(ColumnSizes.CHINESE_COMMON_NAME)
    )
    category = sqlalchemy.Column(sqlalchemy.String(ColumnSizes.CATEGORY))
    order = sqlalchemy.Column(sqlalchemy.String(ColumnSizes.ORDER))
    family_name = sqlalchemy.Column(sqlalchemy.String(ColumnSizes.FAMILY_NAME))
    family_latin_name = sqlalchemy.Column(
        sqlalchemy.String(ColumnSizes.FAMILY_LATIN_NAME)
    )
    taiwan_status = sqlalchemy.Column(sqlalchemy.String(ColumnSizes.TAIWAN_STATUS))
    matzu_status = sqlalchemy.Column(sqlalchemy.String(ColumnSizes.MATZU_STATUS))
    kinmen_status = sqlalchemy.Column(sqlalchemy.String(ColumnSizes.KINMEN_STATUS))
    pratas_status = sqlalchemy.Column(sqlalchemy.String(ColumnSizes.PRATAS_STATUS))
    endemism = sqlalchemy.Column(sqlalchemy.String(ColumnSizes.ENDEMISM))
    conservation_status = sqlalchemy.Column(sqlalchemy.Enum(enums.ConservationStatus))
    codes = sqlalchemy.Column(postgresql.ARRAY(sqlalchemy.String(10)))
