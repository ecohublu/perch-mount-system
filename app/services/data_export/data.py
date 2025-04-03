import sqlalchemy
import sqlalchemy.orm

from app.services import db
from app import model


_AI_SPECIES = sqlalchemy.alias(model.Species)
_HUMAN_SPECIES = sqlalchemy.alias(model.Species)


_DEFAULT_FIELDS = (
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
        model.Species.english_common_name,
        model.Species.scientific_name,
        model.Species.family_name,
        model.Species.category,
        model.Species.order,
        model.Species.taiwan_status,
        model.Species.endemism,
        model.Species.conservation_status,
    ),
    "prey": (
        model.MarkedPreyIndividualsContents.has_prey,
        model.IdentifiedPreyIndividualsContents.inaturalist_taxa_id.label(
            "prey_inat_taxa_id"
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


def get_data(additional_field_sets: list[str], offset: int = 0, limit: int = 100):
    additional_fields = _get_fields_by_sets(additional_field_sets)

    return


def _get_fields_by_sets(sets: list[str]) -> list:
    fields = []
    for s in sets:
        if s not in _FIELDS_SETS:
            continue
        fields.extend(_FIELDS_SETS[s])
    return fields
