from app.services import db
from app import model
import uuid


def get_projects() -> list[model.Projects]:
    with db.session.begin() as session:
        projects = session.query(model.Projects).all()
    return projects


def get_projects_by_ids(ids: list[str]) -> list[model.Projects]:
    ids = list(map(uuid.UUID, ids))
    with db.session.begin() as session:
        projects = (
            session.query(model.Projects).filter(model.Projects.id.in_(ids)).all()
        )
    return projects


def get_project_by_id(project_id: uuid.UUID) -> model.Projects | None:
    with db.session.begin() as session:
        project = (
            session.query(model.Projects)
            .filter(model.Projects.id == project_id)
            .first()
        )
    return project


def add_project(name: str) -> str:
    new_project = model.Projects(name=name)
    with db.session.begin() as session:
        session.add(new_project)
        session.commit()
    return new_project.id
