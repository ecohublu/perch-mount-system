import uuid

from app import model
from app.services import perchai
from app.model import enums


def get_members() -> list[model.Members]:
    with perchai.session.begin() as session:
        query = session.query(model.Members)
        members = query.all()
    return members


def get_member_by_id(member_id: uuid.UUID):
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
) -> int:
    project_id = uuid.UUID(project_id)

    new_member = model.Members(
        gmail=gmail,
        user_name=user_name,
        first_name=first_name,
        last_name=last_name,
        position=position
    )
    with perchai.session.begin() as session:
        session.add(new_member)
        session.commit()
        new_id = new_member.id
    return new_id
