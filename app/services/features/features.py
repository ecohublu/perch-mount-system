from datetime import datetime
import uuid

from app.services import db
from app import model


def get_featrues_media(
    featured_by_id: uuid.UUID = None,
    medium_datetime_from: datetime = None,
    medium_datetime_to: datetime = None,
    behavior_ids: list[uuid.UUID] = [],
    project_ids: list[uuid.UUID] = [],
    perch_mount_ids: list[uuid.UUID] = [],
    taxon_orders: list[int] = [],
    offset: int = 0,
    limit: int = 50,
) -> tuple[int, list[model.Media]]:

    with db.session.begin() as session:
        query = (
            session.query(model.Media)
            .filter(model.Media.status == model.enums.MediaStatus.REVIEWED)
            .filter(model.ReviewedMediaContents.behavior_id != None)
        )
        if featured_by_id:
            query = query.filter(
                model.ReviewedMediaContents.featured_by_id == featured_by_id
            )
        if medium_datetime_from:
            query = query.filter(model.Media.medium_datetime >= medium_datetime_from)
        if medium_datetime_to:
            query = query.filter(model.Media.medium_datetime < medium_datetime_to)
        if behavior_ids:
            query = query.filter(
                model.ReviewedMediaContents.behavior_id.in_(behavior_ids)
            )
        if project_ids:
            query = query.filter(model.PerchMounts.project_id.in_(project_ids))
        if perch_mount_ids:
            query = query.filter(model.PerchMounts.id.in_(perch_mount_ids))
        if taxon_orders:
            query = query.filter(
                model.ReviewedIndividualsContents.taxon_order_by_human.in_(taxon_orders)
            )
        query = query.join(
            model.ReviewedMediaContents,
            model.ReviewedMediaContents.medium_id == model.Media.id,
            isouter=True,
        )
        query = query.join(
            model.Individuals,
            model.Individuals.medium_id == model.Media.id,
            isouter=True,
        )
        query = query.join(
            model.ReviewedIndividualsContents,
            model.ReviewedIndividualsContents.individual_id == model.Individuals.id,
            isouter=True,
        )
        query = query.join(
            model.Sections,
            model.Media.section_id == model.Sections.id,
            isouter=True,
        )
        query = query.join(
            model.PerchMounts,
            model.PerchMounts.id == model.Sections.perch_mount_id,
            isouter=True,
        )
        count = query.count()
        query = query.offset(offset).limit(limit)
    return count, query.all()


def get_featrues_media_counts(
    featured_by_id: uuid.UUID = None,
    medium_datetime_from: datetime = None,
    medium_datetime_to: datetime = None,
    behavior_ids: list[uuid.UUID] = [],
    project_ids: list[uuid.UUID] = [],
    perch_mount_ids: list[uuid.UUID] = [],
    taxon_orders: list[int] = [],
) -> int:

    with db.session.begin() as session:
        query = session.query(model.Media.id).filter(
            model.Media.status == model.enums.MediaStatus.REVIEWED
        )
        if featured_by_id:
            query = query.filter(
                model.ReviewedMediaContents.featured_by_id == featured_by_id
            )
        if medium_datetime_from:
            query = query.filter(model.Media.medium_datetime >= medium_datetime_from)
        if medium_datetime_to:
            query = query.filter(model.Media.medium_datetime < medium_datetime_to)
        if behavior_ids:
            query = query.filter(
                model.ReviewedMediaContents.behavior_id.in_(behavior_ids)
            )
        if project_ids:
            query = query.filter(model.PerchMounts.project_id.in_(project_ids))
        if perch_mount_ids:
            query = query.filter(model.PerchMounts.id.in_(perch_mount_ids))
        if taxon_orders:
            query = query.filter(
                model.ReviewedIndividualsContents.taxon_order_by_human.in_(taxon_orders)
            )

        query = query.join(
            model.ReviewedMediaContents,
            model.ReviewedMediaContents.medium_id == model.Media.id,
            isouter=True,
        )
        query = query.join(
            model.Individuals,
            model.Individuals.medium_id == model.Media.id,
            isouter=True,
        )
        query = query.join(
            model.ReviewedIndividualsContents,
            model.ReviewedIndividualsContents.individual_id == model.Individuals.id,
            isouter=True,
        )
        query = query.join(
            model.Sections,
            model.Media.section_id == model.Sections.id,
            isouter=True,
        )
        query = query.join(
            model.PerchMounts,
            model.PerchMounts.id == model.Sections.perch_mount_id,
            isouter=True,
        )
    return query.count()
