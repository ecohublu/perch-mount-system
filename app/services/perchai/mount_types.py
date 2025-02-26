from app.services import perchai
from app import model
import uuid


def get_mount_types() -> list[model.MountTypes]:
    with perchai.session.begin() as session:
        mount_types = session.query(model.MountTypes).all()
    return mount_types


def get_mount_type_by_id(mount_type_id: uuid.UUID) -> model.MountTypes | None:
    with perchai.session.begin() as session:
        mount_type = (
            session.query(model.MountTypes)
            .filter(model.MountTypes.id == mount_type_id)
            .one_or_none()
        )
    return mount_type


def get_mount_types_by_ids(ids: list[uuid.UUID]) -> list[model.MountTypes]:
    with perchai.session.begin() as session:
        mount_types = (
            session.query(model.MountTypes).filter(model.MountTypes.id.in_(ids)).all()
        )
    return mount_types


def add_mount_types(name: str) -> uuid.UUID:
    new_mount_type = model.MountTypes(name=name)
    with perchai.session.begin() as session:
        session.add(new_mount_type)
        session.commit()
    return new_mount_type.id
