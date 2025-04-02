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


# TODO make sure this function return boolean | None
def is_perch_mount_activated(perch_mount_id: uuid.UUID) -> bool | None:
    with db.session.begin() as session:
        terminated = (
            session.query(model.PerchMounts.terminated)
            .filter(model.PerchMounts.id == perch_mount_id)
            .one_or_none()
        )
    return terminated
