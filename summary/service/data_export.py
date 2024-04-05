import datetime
import service
import sqlalchemy
import sqlalchemy.orm
from src import model


_AI_SPECIES = sqlalchemy.alias(model.Species)
_HUMAN_SPECIES = sqlalchemy.alias(model.Species)

_MEDIA_COLUMNS = (
    model.Projects.name,
    model.PerchMounts.perch_mount_name,
    model.PerchMounts.habitat,
    model.PerchMounts.latitude,
    model.PerchMounts.longitude,
    model.PerchMounts.layer,
    model.Sections.camera,
    model.Media.medium_datetime,
    model.Individuals.prey,
    model.Individuals.prey_name,
    model.Individuals.ring_number,
    model.Individuals.xmax,
    model.Individuals.xmin,
    model.Individuals.ymax,
    model.Individuals.ymin,
    _AI_SPECIES.c.chinese_common_name.label("chinese_common_name_by_ai"),
    _AI_SPECIES.c.scientific_name.label("scientific_name_by_ai"),
    _AI_SPECIES.c.taxon_order.label("taxon_order_by_ai"),
    _HUMAN_SPECIES.c.chinese_common_name.label("chinese_common_name_by_human"),
    _HUMAN_SPECIES.c.scientific_name.label("scientific_name_by_human"),
    _HUMAN_SPECIES.c.taxon_order.label("taxon_order_by_human"),
)

_DETECTED_COLUMNS = (
    model.Projects.name,
    model.PerchMounts.perch_mount_name,
    model.PerchMounts.habitat,
    model.PerchMounts.latitude,
    model.PerchMounts.longitude,
    model.PerchMounts.layer,
    model.Sections.camera,
    model.DetectedMedia.medium_datetime,
    model.DetectedIndividuals.xmax,
    model.DetectedIndividuals.xmin,
    model.DetectedIndividuals.ymax,
    model.DetectedIndividuals.ymin,
    _AI_SPECIES.c.chinese_common_name.label("chinese_common_name_by_ai"),
    _AI_SPECIES.c.scientific_name.label("scientific_name_by_ai"),
    _AI_SPECIES.c.taxon_order.label("taxon_order_by_ai"),
)


def get_export_data(
    project_ids: list[int] = [],
    perch_mount_ids: list[int] = [],
    section_ids: list[int] = [],
    start_time: datetime.datetime = None,
    end_time: datetime.datetime = None,
    prey: bool = None,
    prey_names: list[str] = None,
    taxon_orders_by_human: list[int] = [],
    taxon_orders_by_ai: list[int] = [],
    unreviewed_data: bool = False,
):
    with service.session.begin() as session:
        media_query = session.query(*_MEDIA_COLUMNS)
        media_query = _join_tables(media_query)
        media_query = _find_by_conditions(
            media_query,
            model.Media,
            model.Individuals,
            project_ids,
            perch_mount_ids,
            section_ids,
            start_time,
            end_time,
            prey,
            prey_names,
            taxon_orders_by_human,
            taxon_orders_by_ai,
        )

        if unreviewed_data:
            detected_query = session.query(*_DETECTED_COLUMNS)
            detected_query = _find_by_conditions(
                detected_query,
                model.DetectedMedia,
                model.DetectedIndividuals,
                project_ids,
                perch_mount_ids,
                section_ids,
                start_time,
                end_time,
                prey,
                prey_names,
                taxon_orders_by_human,
                taxon_orders_by_ai,
            )
            media_query = media_query.union(detected_query)

    results = media_query.all()
    return results


def _join_tables(query: sqlalchemy.orm.Query):
    query = query.join(
        model.Media,
        model.Media.medium_id == model.Individuals.medium,
    )
    query = query.join(
        model.Sections,
        model.Sections.section_id == model.Media.section,
    )
    query = query.join(
        model.PerchMounts,
        model.PerchMounts.perch_mount_id == model.Sections.perch_mount,
    )
    query = query.join(
        _AI_SPECIES,
        _AI_SPECIES.c.taxon_order == model.Individuals.taxon_order_by_ai,
    )
    query = query.join(
        _HUMAN_SPECIES,
        _HUMAN_SPECIES.c.taxon_order == model.Individuals.taxon_order_by_human,
    )
    return query


def _find_by_conditions(
    query: sqlalchemy.orm.Query,
    media: model.Media | model.DetectedMedia,
    individuals: model.Individuals | model.DetectedIndividuals,
    project_ids: list[int] = [],
    perch_mount_ids: list[int] = [],
    section_ids: list[int] = [],
    start_time: datetime.datetime = None,
    end_time: datetime.datetime = None,
    prey: bool = None,
    prey_names: list[str] = None,
    taxon_orders_by_human: list[int] = [],
    taxon_orders_by_ai: list[int] = [],
):
    if project_ids:
        query = query.filter(model.Projects.project_id.in_(project_ids))

    if perch_mount_ids:
        query = query.filter(model.PerchMounts.perch_mount_id.in_(perch_mount_ids))

    if section_ids:
        query = query.filter(model.Sections.section_id.in_(section_ids))

    if start_time:
        query = query.filter(media.medium_datetime >= start_time)

    if end_time:
        query = query.filter(media.medium_datetime < end_time)

    if prey is not None:
        query = query.filter(individuals.prey == prey)

    if prey_names:
        query = query.filter(individuals.prey_name.in_(prey_names))

    if taxon_orders_by_human and individuals.__name__ == "Individuals":
        query = query.filter(
            individuals.taxon_order_by_human.in_(taxon_orders_by_human)
        )

    if taxon_orders_by_ai:
        query = query.filter(individuals.taxon_order_by_ai.in_(taxon_orders_by_ai))

    return query
