import sqlalchemy
import sqlalchemy.orm
import uuid


from app.services import db
import app.services.perchai.utils as services_utils
from app import model
from app.model import enums


def get_perch_mounts_by_filter(
    filter: services_utils.PerchMountFilter,
) -> list[model.PerchMounts]:
    modifier = services_utils.PerchMountQueryModifier(filter)
    with db.session.begin() as session:
        query = session.query(model.PerchMounts)
        query = modifier.filter_query(query)
        perch_mounts = query.all()
    return perch_mounts


def get_perch_mount_by_id(perch_mount_id: uuid.UUID) -> model.PerchMounts | None:
    with db.session.begin() as session:
        perch_mount = (
            session.query(model.PerchMounts)
            .filter(model.PerchMounts.id == perch_mount_id)
            .one_or_none()
        )
    return perch_mount


def add_perch_mount(
    perch_mount_name: str,
    latitude: float,
    longitude: float,
    project_id: uuid.UUID,
    habitat: str | enums.Habitats,
    mount_layer: str | enums.MountLayers,
    note: str = None,
) -> uuid.UUID:

    new_perch_mount = model.PerchMounts(
        perch_mount_name=perch_mount_name,
        latitude=latitude,
        longitude=longitude,
        habitat=habitat.upper(),
        project_id=project_id,
        mount_layer=mount_layer.upper(),
        note=note,
    )
    with db.session.begin() as session:
        session.add(new_perch_mount)
        session.commit()
        new_id = new_perch_mount.id
    return new_id


def update_perch_mount(perch_mount_id: uuid.UUID, arg: dict):
    with db.session.begin() as session:
        session.query(model.PerchMounts).filter(
            model.PerchMounts.id == perch_mount_id
        ).update(arg)
        session.commit()


def terminate_perch_mount(perch_mount_id: uuid.UUID):
    with db.session.begin() as session:
        session.query(model.PerchMounts).filter(
            model.PerchMounts.id == perch_mount_id
        ).update({"terminated": True})
        session.commit()


def activate_perch_mount(perch_mount_id: uuid.UUID):
    with db.session.begin() as session:
        session.query(model.PerchMounts).filter(
            model.PerchMounts.id == perch_mount_id
        ).update({"terminated": False})
        session.commit()


def is_perch_mount_activated(perch_mount_id: uuid.UUID) -> bool | None:
    with db.session.begin() as session:
        terminated = (
            session.query(model.PerchMounts.terminated)
            .filter(model.PerchMounts.id == perch_mount_id)
            .one_or_none()
        )
    return terminated


def get_perch_mounts_pending_counts() -> list:
    with db.session.begin() as session:
        query = _perch_mounts_pending_counts_query(session)
    return query.all()


def get_perch_mount_pending_counts_by_id(perch_mount_id: uuid.UUID) -> list:
    with db.session.begin() as session:
        query = _perch_mounts_pending_counts_query(
            session, perch_mount_id=perch_mount_id
        )
    return query.one_or_none()


def _perch_mounts_pending_counts_query(
    session: sqlalchemy.orm.Session, perch_mount_id: uuid.UUID = None
) -> sqlalchemy.orm.Query:

    pending_counts_query = (
        session.query(
            model.PerchMounts.id,
            model.PerchMounts.perch_mount_name,
            model.PerchMounts.claim_by_id,
            model.PerchMounts.is_priority,
            sqlalchemy.func.coalesce(
                sqlalchemy.func.sum(model.Sections.undetected_count), 0
            ).label("undetected_count"),
            sqlalchemy.func.coalesce(
                sqlalchemy.func.sum(model.Sections.unchecked_count), 0
            ).label("unchecked_count"),
            sqlalchemy.func.coalesce(
                sqlalchemy.func.sum(model.Sections.unreviewed_count), 0
            ).label("unreviewed_count"),
            sqlalchemy.func.coalesce(
                sqlalchemy.func.sum(model.Sections.reviewed_count), 0
            ).label("reviewed_count"),
            sqlalchemy.func.coalesce(
                sqlalchemy.func.sum(model.Sections.accidental_count), 0
            ).label("accidental_count"),
        )
        .select_from(model.PerchMounts)
        .outerjoin(
            model.Sections,
            model.PerchMounts.id == model.Sections.perch_mount_id,
        )
        .group_by(
            model.PerchMounts.id,
            model.PerchMounts.perch_mount_name,
        )
        .subquery()
    )

    query = session.query(
        pending_counts_query.c.id,
        pending_counts_query.c.perch_mount_name,
        pending_counts_query.c.claim_by_id,
        pending_counts_query.c.is_priority,
        model.Members.display_name.label("claimer_name"),
        model.Members.profile_picture_url.label("claim_picture_url"),
        pending_counts_query.c.undetected_count,
        pending_counts_query.c.unchecked_count,
        pending_counts_query.c.unreviewed_count,
        pending_counts_query.c.reviewed_count,
        pending_counts_query.c.accidental_count,
    ).join(
        model.Members,
        model.Members.id == pending_counts_query.c.claim_by_id,
        isouter=True,
    )

    if perch_mount_id:
        query = query.filter(pending_counts_query.c.id == perch_mount_id)

    return query
