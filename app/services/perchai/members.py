import sqlalchemy
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


def get_member_by_sub_and_gmail(sub: str, email: str) -> model.Members | None:
    with perchai.session.begin() as session:
        member = (
            session.query(model.Members)
            .filter(
                sqlalchemy.or_(
                    model.Members.oidc_sub == sub,
                    model.Members.gmail == email,
                )
            )
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


def update_member_sso_info(id_token_info: dict):
    with perchai.session.begin() as session:
        session.query(model.Members).filter(
            sqlalchemy.or_(
                model.Members.oidc_sub == id_token_info["sub"],
                model.Members.gmail == id_token_info["email"],
            )
        ).update(
            {
                "oidc_usb": id_token_info["sub"],
                "display_name": id_token_info["name"],
                "first_name": id_token_info["given_name"],
                "last_name": id_token_info["family_name"],
                "profile_picture_url": id_token_info["picture"],
            }
        )
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
