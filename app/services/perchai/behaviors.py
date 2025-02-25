from app.services import perchai
from app import model
import uuid


def get_behaviors() -> list[model.Behaviors]:
    with perchai.session.begin() as session:
        behaviors = session.query(model.Behaviors).all()
    return behaviors


def get_behavior_by_id(behavior_id: str) -> model.Behaviors | None:
    behavior_id = uuid.UUID(behavior_id)
    with perchai.session.begin() as session:
        behavior = (
            session.query(model.Behaviors)
            .filter(model.Behaviors.id == behavior_id)
            .one()
        )
    return behavior


def add_behavior(name: str) -> str:
    new_behavior = model.Behaviors(name=name)
    with perchai.session.begin() as session:
        session.add(new_behavior)
        session.commit()
    return new_behavior.id
