import uuid

from app import model
from app.services import perchai
from app.model import enums
from app.error_handler import errors


def get_members() -> list[model.Members]:
    with perchai.session.begin() as session:
        query = session.query(model.Members)
        members = query.all()
    return members


def get_member_by_id(member_id: uuid.UUID) -> model.Members | None:
    with perchai.session.begin() as session:
        member = (
            session.query(model.Members)
            .filter(model.Members.id == member_id)
            .one_or_none()
        )
    return member


def add_member(
    gmail: str,
    user_name: str,
    first_name: str,
    last_name: str,
    position: enums.Positions,
) -> uuid.UUID:

    new_member = model.Members(
        gmail=gmail,
        user_name=user_name,
        first_name=first_name,
        last_name=last_name,
        position=position,
    )
    with perchai.session.begin() as session:
        session.add(new_member)
        session.commit()
        new_id = new_member.id
    return new_id


def update_member(member_id: uuid.UUID, args: dict):
    with perchai.session.begin() as session:
        session.query(model.Members).filter(model.Members.id == member_id).update(args)
        session.commit()


def block_member(member_id: uuid.UUID):
    with perchai.session.begin() as session:
        member: model.Members = (
            session.query(model.Members.is_super_admin)
            .filter(model.Members.id == member_id)
            .one_or_none()
        )

        if member.is_super_admin:
            raise errors.SuperAdminUnpatchableError

        session.query(model.Members).filter(model.Members.id == member_id).update(
            {"blocked": True}
        )
        session.commit()


def unblock_member(member_id: uuid.UUID):
    with perchai.session.begin() as session:
        session.query(model.Members).filter(model.Members.id == member_id).update(
            {"blocked": False}
        )
        session.commit()


def activate_member(member_id: uuid.UUID):
    with perchai.session.begin() as session:
        member: model.Members = (
            session.query(model.Members.is_super_admin)
            .filter(model.Members.id == member_id)
            .one_or_none()
        )

        if member.is_super_admin:
            raise errors.SuperAdminUnpatchableError

        session.query(model.Members).filter(model.Members.id == member_id).update(
            {"activated": True}
        )
        session.commit()


def deactivate_member(member_id: uuid.UUID):
    with perchai.session.begin() as session:
        member: model.Members = (
            session.query(model.Members.is_super_admin)
            .filter(model.Members.id == member_id)
            .one_or_none()
        )

        if member.is_super_admin:
            raise errors.SuperAdminUnpatchableError

        session.query(model.Members).filter(model.Members.id == member_id).update(
            {"activated": False}
        )
        session.commit()
