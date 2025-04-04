from datetime import datetime
import uuid
import sqlalchemy
import sqlalchemy.orm

from app.services import db
from app import model


_AI_SPECIES = sqlalchemy.alias(model.Species)
_HUMAN_SPECIES = sqlalchemy.alias(model.Species)


_DEFAULT_FIELDS = (
    model.Individuals.id,
    model.Projects.name,
    model.PerchMounts.perch_mount_name,
    model.Sections.swapped_date,
    model.Media.medium_datetime,
    model.UnreviewedIndividualsContents.taxon_order_by_ai,
    model.ReviewedIndividualsContents.taxon_order_by_human,
    model.Species.chinese_common_name,
    _AI_SPECIES.c.chinese_common_name.label("chinese_common_name_by_ai"),
    _HUMAN_SPECIES.c.chinese_common_name.label("chinese_common_name_by_human"),
)

_FIELDS_SETS = {
    "perch_mount": (
        model.PerchMounts.longitude,
        model.PerchMounts.latitude,
        model.PerchMounts.habitat,
        model.PerchMounts.mount_layer,
    ),
    "section": (
        model.MountTypes.name.label("mount_type"),
        model.Cameras.model_name.label("camera"),
        model.Sections.start_time,
        model.Sections.end_time,
    ),
    "species": (
        _AI_SPECIES.c.taxon_order.label("taxon_order_by_ai"),
        _HUMAN_SPECIES.c.taxon_order.label("taxon_order_by_human"),
        _AI_SPECIES.c.english_common_name.label("english_common_name_by_ai"),
        _HUMAN_SPECIES.c.english_common_name.label("english_common_name_by_human"),
        _AI_SPECIES.c.scientific_name.label("scientific_name_by_ai"),
        _HUMAN_SPECIES.c.scientific_name.label("scientific_name_by_human"),
    ),
    "prey": (
        model.MarkedPreyIndividualsContents.has_prey,
        model.IdentifiedPreyIndividualsContents.inaturalist_taxa_id.label(
            "prey_inat_id"
        ),
    ),
    "tag": (
        model.TaggedIndividualsContents.is_tagged,
        model.TaggedIndividualsContents.has_ring,
        model.TaggedIndividualsContents.ring_number,
    ),
    "yolo": (
        model.UnreviewedIndividualsContents.box_xmax.label("unreviewed_xmax"),
        model.UnreviewedIndividualsContents.box_xmin.label("unreviewed_xmin"),
        model.UnreviewedIndividualsContents.box_ymax.label("unreviewed_ymax"),
        model.UnreviewedIndividualsContents.box_ymin.label("unreviewed_ymin"),
        model.ReviewedIndividualsContents.box_xmax.label("reviewed_xmax"),
        model.ReviewedIndividualsContents.box_xmin.label("reviewed_xmin"),
        model.ReviewedIndividualsContents.box_ymax.label("reviewed_ymax"),
        model.ReviewedIndividualsContents.box_ymin.label("reviewed_ymin"),
    ),
}


class DataExportQueryHelper:
    def __init__(
        self,
        field_sets: list[str] = None,
        projects: list[uuid.UUID] = None,
        perch_mounts: list[uuid.UUID] = None,
        habitats: list[str] = None,
        cameras: list[uuid.UUID] = None,
        mount_types: list[uuid.UUID] = None,
        medium_datetime_from: datetime = None,
        medium_datetime_to: datetime = None,
        taxon_orders: list[int] = None,
        has_prey: bool = None,
        inaturalist_taxa_ids: list[int] = None,
        tagged: bool = None,
        included_unreviewed: bool = None,
    ):
        self.field_sets = field_sets
        self.projects = projects
        self.perch_mounts = perch_mounts
        self.habitats = habitats
        self.cameras = cameras
        self.mount_types = mount_types
        self.medium_datetime_from = medium_datetime_from
        self.medium_datetime_to = medium_datetime_to
        self.taxon_orders = taxon_orders
        self.has_prey = has_prey
        self.inaturalist_taxa_ids = inaturalist_taxa_ids
        self.tagged = tagged
        self.included_unreviewed = included_unreviewed

    def get_fields_by_sets(self) -> list:
        fields = []
        if self.field_sets:
            for s in self.field_sets:
                if s not in _FIELDS_SETS:
                    continue
                fields.extend(_FIELDS_SETS[s])
        return fields

    def join_query(self, query: sqlalchemy.orm.Query) -> sqlalchemy.orm.Query:

        query = (
            query.join(
                model.MarkedPreyIndividualsContents,
                model.Individuals.id
                == model.MarkedPreyIndividualsContents.individual_id,
            )
            .join(
                model.IdentifiedPreyIndividualsContents,
                model.Individuals.id
                == model.IdentifiedPreyIndividualsContents.individual_id,
            )
            .join(
                model.TaggedIndividualsContents,
                model.Individuals.id == model.TaggedIndividualsContents.individual_id,
            )
            .join(
                model.UnreviewedIndividualsContents,
                model.Individuals.id
                == model.UnreviewedIndividualsContents.individual_id,
            )
            .join(
                model.ReviewedIndividualsContents,
                model.Individuals.id == model.ReviewedIndividualsContents.individual_id,
            )
            .join(
                _AI_SPECIES,
                _AI_SPECIES.c.taxon_order
                == model.UnreviewedIndividualsContents.taxon_order_by_ai,
            )
            .join(
                _HUMAN_SPECIES,
                _HUMAN_SPECIES.c.taxon_order
                == model.ReviewedIndividualsContents.taxon_order_by_human,
            )
            .join(model.Media, model.Individuals.medium_id == model.Media.id)
            .join(model.Sections, model.Media.section_id == model.Sections.id)
            .join(model.Cameras, model.Sections.camera_id == model.Cameras.id)
            .join(model.MountTypes, model.Sections.mount_type_id == model.MountTypes.id)
            .join(
                model.PerchMounts,
                model.Sections.perch_mount_id == model.PerchMounts.id,
            )
            .join(model.Projects, model.PerchMounts.project_id == model.Projects.id)
        )

        return query

    def filter_query(self, query: sqlalchemy.orm.Query) -> sqlalchemy.orm.Query:
        if self.projects:
            query = query.filter(model.Projects.id.in_(self.projects))
        if self.perch_mounts:
            query = query.filter(model.PerchMounts.id.in_(self.perch_mounts))
        if self.habitats:
            query = query.filter(model.PerchMounts.habitat.in_(self.habitats))
        if self.cameras:
            query = query.filter(model.Cameras.id.in_(self.cameras))
        if self.mount_types:
            query = query.filter(model.MountTypes.id.in_(self.mount_types))
        if self.medium_datetime_from:
            query = query.filter(
                model.Media.medium_datetime >= self.medium_datetime_from
            )
        if self.medium_datetime_to:
            query = query.filter(model.Media.medium_datetime < self.medium_datetime_to)

        if self.included_unreviewed and self.taxon_orders:
            query = query.filter(
                sqlalchemy.or_(
                    model.ReviewedIndividualsContents.taxon_order_by_human.in_(
                        self.taxon_orders
                    ),
                    sqlalchemy.and_(
                        model.UnreviewedIndividualsContents.taxon_order_by_ai.in_(
                            self.taxon_orders
                        ),
                        model.ReviewedIndividualsContents.taxon_order_by_human == None,
                    ),
                )
            )
        elif self.taxon_orders:
            query = query.filter(
                model.ReviewedIndividualsContents.taxon_order_by_human.in_(
                    self.taxon_orders
                )
            )

        if self.has_prey is not None:
            query = query.filter(
                model.MarkedPreyIndividualsContents.has_prey == self.has_prey
            )
        if self.inaturalist_taxa_ids:
            query = query.filter(
                model.IdentifiedPreyIndividualsContents.inaturalist_taxa_id.in_(
                    self.inaturalist_taxa_ids
                )
            )
        return query


def get_data(helper: DataExportQueryHelper, offset: int = 0, limit: int = None):
    additional_fields = helper.get_fields_by_sets()
    print(additional_fields)
    with db.session.begin() as session:
        query = session.query(*_DEFAULT_FIELDS, *additional_fields)
        query = helper.join_query(query)
        query = helper.filter_query(query)
        query = query.offset(offset)
        if limit:
            query = query.limit(limit)
        data = query.all()
    return data
