import sqlalchemy
from sqlalchemy.dialects import postgresql

import extensions
from app.model import enums
from app.model import utils


class Species(extensions.db.Model, utils.JsonAbleModel):
    __tablename__ = "species"
    taxon_order = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    scientific_name = sqlalchemy.Column(sqlalchemy.String(100))
    english_common_name = sqlalchemy.Column(sqlalchemy.String(100))
    chinese_common_name = sqlalchemy.Column(sqlalchemy.String(50))
    category = sqlalchemy.Column(sqlalchemy.String(15))
    order = sqlalchemy.Column(sqlalchemy.String(50))
    family_name = sqlalchemy.Column(sqlalchemy.String(50))
    family_latin_name = sqlalchemy.Column(sqlalchemy.String(50))
    taiwan_status = sqlalchemy.Column(sqlalchemy.String(50))
    matzu_status = sqlalchemy.Column(sqlalchemy.String(50))
    kinmen_status = sqlalchemy.Column(sqlalchemy.String(50))
    pratas_status = sqlalchemy.Column(sqlalchemy.String(50))
    endemism = sqlalchemy.Column(sqlalchemy.String(50))
    conservation_status = sqlalchemy.Column(sqlalchemy.Enum(enums.ConservationStatus))
    codes = sqlalchemy.Column(postgresql.ARRAY(sqlalchemy.String(10)))
