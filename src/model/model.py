import uuid
from datetime import datetime, date
import sqlalchemy
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects import postgresql
import src.utils
import src.model.enums

db = SQLAlchemy()
migrate = Migrate()


PERCH_MOUNT_NAME_MAX_LENGTH = 15


class JsonAbleModel:
    def to_json(self):
        json = {}
        for c in self.__table__.columns:
            value = getattr(self, c.name)

            if type(value) == datetime or type(value) == date:
                value = value.isoformat()

            json[c.name] = value

        return json


class PerchMounts(db.Model, JsonAbleModel):
    __tablename__ = "perch_mounts"
    id = sqlalchemy.Column(
        postgresql.UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    perch_mount_name = sqlalchemy.Column(
        sqlalchemy.String(PERCH_MOUNT_NAME_MAX_LENGTH),
        unique=True,
        nullable=False,
    )
    longitude = sqlalchemy.Column(sqlalchemy.Float, nullable=False)
    latitude = sqlalchemy.Column(sqlalchemy.Float, nullable=False)
    habitat = sqlalchemy.Column(sqlalchemy.Enum(src.model.enums.Habitats))
    project_id = sqlalchemy.Column(
        postgresql.UUID(as_uuid=True),
        sqlalchemy.ForeignKey("projects.id"),
        nullable=False,
    )
    claim_by_id = sqlalchemy.Column(
        postgresql.UUID(as_uuid=True),
        sqlalchemy.ForeignKey("members.member_id"),
    )
    layer = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("mount_layers.id"), nullable=False
    )
    terminated = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    is_priority = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    note = sqlalchemy.Column(sqlalchemy.Text)


class Sections(db.Model, JsonAbleModel):
    __tablename__ = "sections"
    id = sqlalchemy.Column(
        postgresql.UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    perch_mount_id = sqlalchemy.Column(
        postgresql.UUID(as_uuid=True),
        sqlalchemy.ForeignKey("perch_mounts.id"),
        nullable=False,
    )
    mount_type_id = sqlalchemy.Column(
        postgresql.UUID(as_uuid=True),
        sqlalchemy.ForeignKey("mount_types.id"),
        nullable=False,
    )
    camera_id = sqlalchemy.Column(
        postgresql.UUID(as_uuid=True),
        sqlalchemy.ForeignKey("cameras.id"),
        nullable=False,
    )
    swapped_date = sqlalchemy.Column(
        sqlalchemy.Date,
        nullable=False,
    )
    valid = sqlalchemy.Column(
        sqlalchemy.Boolean,
        default=True,
        nullable=False,
    )
    note = sqlalchemy.Column(sqlalchemy.Text)


class SectionOperators(db.Model, JsonAbleModel):
    __tablename__ = "section_swappers"
    section_id = sqlalchemy.Column(
        postgresql.UUID(as_uuid=True),
        sqlalchemy.ForeignKey("sections.id"),
        primary_key=True,
        nullable=False,
    )
    swapper_id = sqlalchemy.Column(
        postgresql.UUID(as_uuid=True),
        sqlalchemy.ForeignKey("members.id"),
        primary_key=True,
        nullable=False,
    )


class Media(db.Model, JsonAbleModel):
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
        sqlalchemy.ForeignKey("sections.id"),
        nullable=False,
    )
    medium_datetime = sqlalchemy.Column(sqlalchemy.DateTime)
    created_at = sqlalchemy.Column(
        sqlalchemy.DateTime,
        default=sqlalchemy.sql.func.now(),
        nullable=False,
    )
    medium_type = sqlalchemy.Column(sqlalchemy.Enum(src.model.enums.MediaType))
    nas_path = sqlalchemy.Column(sqlalchemy.String(255))
    # status create by migration sql.


class EmptyMedia(db.Model, JsonAbleModel):
    __tablename__ = "empty_media"
    empty_medium_id = sqlalchemy.Column(sqlalchemy.String(22), primary_key=True)
    section = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("sections.section_id")
    )
    medium_datetime = sqlalchemy.Column(sqlalchemy.DateTime)
    path = sqlalchemy.Column(sqlalchemy.String(255))
    checked = sqlalchemy.Column(sqlalchemy.Boolean, default=False)


class DetectedMedia(db.Model, JsonAbleModel):
    __tablename__ = "detected_media"
    detected_medium_id = sqlalchemy.Column(sqlalchemy.String(22), primary_key=True)
    section = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("sections.section_id")
    )
    medium_datetime = sqlalchemy.Column(sqlalchemy.DateTime)
    path = sqlalchemy.Column(sqlalchemy.String(255))
    reviewed = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    empty_checker = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("members.member_id")
    )
    empty_checked = sqlalchemy.Column(sqlalchemy.Boolean, default=False)


class Individuals(db.Model, JsonAbleModel):
    __tablename__ = "individuals"
    individual_id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True
    )
    taxon_order_by_ai = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("species.taxon_order")
    )
    taxon_order_by_human = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("species.taxon_order")
    )
    medium = sqlalchemy.Column(
        sqlalchemy.String(22), sqlalchemy.ForeignKey("media.medium_id")
    )
    prey = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    prey_name = sqlalchemy.Column(sqlalchemy.String(15))
    tagged = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    ring_number = sqlalchemy.Column(sqlalchemy.String(15))
    file_type = sqlalchemy.Column(sqlalchemy.String(5))
    xmin = sqlalchemy.Column(sqlalchemy.Float)
    xmax = sqlalchemy.Column(sqlalchemy.Float)
    ymin = sqlalchemy.Column(sqlalchemy.Float)
    ymax = sqlalchemy.Column(sqlalchemy.Float)
    prey_identify_by = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("members.member_id")
    )


class DetectedIndividuals(db.Model, JsonAbleModel):
    __tablename__ = "detected_individuals"
    pending_individual_id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True
    )
    taxon_order_by_ai = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("species.taxon_order")
    )
    medium = sqlalchemy.Column(
        sqlalchemy.String(22),
        sqlalchemy.ForeignKey("detected_media.detected_medium_id"),
    )
    xmin = sqlalchemy.Column(sqlalchemy.Float)
    xmax = sqlalchemy.Column(sqlalchemy.Float)
    ymin = sqlalchemy.Column(sqlalchemy.Float)
    ymax = sqlalchemy.Column(sqlalchemy.Float)


class Members(db.Model, JsonAbleModel):
    __tablename__ = "members"
    member_id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True
    )
    user_name = sqlalchemy.Column(sqlalchemy.String(20), unique=True, nullable=False)
    first_name = sqlalchemy.Column(sqlalchemy.String(50))
    last_name = sqlalchemy.Column(sqlalchemy.String(50))
    position = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("positions.position_id")
    )
    phone_number = sqlalchemy.Column(sqlalchemy.String(10), unique=True, nullable=False)
    is_admin = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    is_super_admin = sqlalchemy.Column(sqlalchemy.Boolean, default=False)


class Contributions(db.Model, JsonAbleModel):
    __tablename__ = "contributions"
    contribution_id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True
    )
    contributor = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("members.member_id")
    )
    num_files = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    action = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("actions.action_id")
    )
    time = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.utcnow)


class Species(db.Model, JsonAbleModel):
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
    conservation_status = sqlalchemy.Column(sqlalchemy.String(5))
    usage_count = sqlalchemy.Column(sqlalchemy.Integer, default=0)


class SpeciesCodes(db.Model, JsonAbleModel):
    __tablename__ = "species_codes"
    taxon_order = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("species.taxon_order"),
        primary_key=True,
    )
    code = sqlalchemy.Column(sqlalchemy.String(10), primary_key=True)


class Behaviors(db.Model, JsonAbleModel):
    __tablename__ = "behaviors"
    behavior_id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True
    )
    chinese_name = sqlalchemy.Column(sqlalchemy.String(20), nullable=False, unique=True)


class Positions(db.Model, JsonAbleModel):
    __tablename__ = "positions"
    position_id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True
    )
    name = sqlalchemy.Column(sqlalchemy.String(20))


class MountTypes(db.Model, JsonAbleModel):
    __tablename__ = "mount_types"
    mount_type_id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True
    )
    name = sqlalchemy.Column(sqlalchemy.String(15))


class Cameras(db.Model, JsonAbleModel):
    __tablename__ = "cameras"
    camera_id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True
    )
    model_name = sqlalchemy.Column(sqlalchemy.String(30))


class Habitats(db.Model, JsonAbleModel):
    __tablename__ = "habitats"
    habitat_id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True
    )
    chinese_name = sqlalchemy.Column(sqlalchemy.String(10))
    english_name = sqlalchemy.Column(sqlalchemy.String(25))


class Projects(db.Model, JsonAbleModel):
    __tablename__ = "projects"
    project_id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True
    )
    name = sqlalchemy.Column(sqlalchemy.String(15))


class Layers(db.Model, JsonAbleModel):
    __tablename__ = "layers"
    layer_id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True
    )
    name = sqlalchemy.Column(sqlalchemy.String(15))


class Events(db.Model, JsonAbleModel):
    __tablename__ = "events"
    event_id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True
    )
    chinese_name = sqlalchemy.Column(sqlalchemy.String(15))
    english_name = sqlalchemy.Column(sqlalchemy.String(15))


class Actions(db.Model, JsonAbleModel):
    __tablename__ = "actions"
    action_id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True
    )
    name = sqlalchemy.Column(sqlalchemy.String(15))


class UpdateInfo(db.Model, JsonAbleModel):
    __tablename__ = "update_info"
    update_info_id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True
    )
    message = sqlalchemy.Column(db.Text)
    detail = sqlalchemy.Column(db.Text)
    create_date = sqlalchemy.Column(sqlalchemy.Date, default=datetime.today)
    checked = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
