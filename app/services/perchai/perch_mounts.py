import uuid

from app.services import perchai
from app.services.perchai.utils import query_filter, query_modifier
from app import model
from app.model import enums


def get_perch_mounts(filter: query_filter.PerchMountFilter) -> list[model.PerchMounts]:
    modifier = query_modifier.PerchMountQueryModifier(filter)
    with perchai.session.begin() as session:
        query = session.query(model.PerchMounts)
        query = modifier.filter_query(query)
        perch_mounts = query.all()
    return perch_mounts


def get_perch_mount_by_id(perch_mount_id: str):
    perch_mount_id = uuid.UUID(perch_mount_id)
    with perchai.session.begin() as session:
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
    project_id: str,
    habitat: str | enums.Habitats,
    mount_layer: str | enums.MountLayers,
    note: str = None,
) -> int:
    project_id = uuid.UUID(project_id)

    new_perch_mount = model.PerchMounts(
        perch_mount_name=perch_mount_name,
        latitude=latitude,
        longitude=longitude,
        habitat=habitat,
        project_id=project_id,
        mount_layer=mount_layer,
        note=note,
    )
    with perchai.session.begin() as session:
        session.add(new_perch_mount)
        session.commit()
        new_id = new_perch_mount.id
    return new_id


def update_perch_mount(perch_mount_id: str, arg: dict):
    perch_mount_id = uuid.UUID(perch_mount_id)
    with perchai.session.begin() as session:
        session.query(model.PerchMounts).filter(
            model.PerchMounts.id == perch_mount_id
        ).update(arg)
        session.commit()
