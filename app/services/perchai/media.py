from datetime import datetime
import uuid
import sqlalchemy
import sqlalchemy.orm

from app.services import perchai
from app.services.perchai.utils import query_filter
from app import model
from app.model import enums


def get_media(filter: query_filter.MediaFilter) -> list[model.Media]:
    with perchai.session.begin() as session:
        query = session.query(
            model.Media.medium_id,
            model.Media.medium_datetime,
            model.Media.section,
            model.Media.path,
            model.Media.empty_checker,
            model.Media.reviewer,
            model.Media.event,
            model.Media.featured_behavior,
            model.Media.featured_by,
            model.Media.featured_title,
            model.Sections.check_date,
            model.PerchMounts.perch_mount_id,
            model.PerchMounts.perch_mount_name,
            model.Projects.name.label("project_name"),
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
            model.Projects,
            model.Projects.project_id == model.PerchMounts.project,
        )

        query = query.order_by(model.Media.medium_datetime)
        query = query.offset(offset).limit(limit)
        results = query.all()

    return results


def get_medium_by_id(medium_id: str) -> model.Media:
    with perchai.session.begin() as session:
        query = session.query(
            model.Media.medium_id,
            model.Media.medium_datetime,
            model.Media.section,
            model.Media.path,
            model.Media.empty_checker,
            model.Media.reviewer,
            model.Media.event,
            model.Media.featured_behavior,
            model.Media.featured_by,
            model.Media.featured_title,
            model.Sections.check_date,
            model.PerchMounts.perch_mount_id,
            model.PerchMounts.perch_mount_name,
            model.Projects.name.label("project_name"),
        ).filter(model.Media.medium_id == medium_id)
        query = query.join(
            model.Sections,
            model.Sections.section_id == model.Media.section,
        )
        query = query.join(
            model.PerchMounts,
            model.PerchMounts.perch_mount_id == model.Sections.perch_mount,
        )
        query = query.join(
            model.Projects,
            model.Projects.project_id == model.PerchMounts.project,
        )
        result = query.one_or_none()

    return result


def update_medium(medium_id: str, arg: dict):
    with perchai.session.begin() as session:
        session.query(model.Media).filter(model.Media.medium_id == medium_id).update(
            arg
        )
        session.commit()


def add_media_and_individuals(media: list[dict]):
    individauls = _get_individauls_from_media(media)
    media = _pop_media_individual(media)
    new_meida: list[model.Media] = []
    new_individuals: list[model.Individuals] = []
    for medium in media:
        new_meida.append(model.Media(**medium))
    for individual in individauls:
        new_individuals.append(model.Individuals(**individual))

    with perchai.session.begin() as session:
        try:
            session.add_all(new_meida)
            session.flush()
            session.add_all(new_individuals)
            session.commit()
        except:
            session.rollback()
            raise


def _get_individauls_from_media(media: list[dict]) -> list[dict]:
    individuals = []
    for medium in media:
        for individual in medium["individuals"]:
            individual["medium"] = medium["medium_id"]
            individuals.append(individual)
    return individuals


def _pop_media_individual(media: list[dict]) -> list[dict]:
    for medium in media:
        medium.pop("individuals")
    return media
