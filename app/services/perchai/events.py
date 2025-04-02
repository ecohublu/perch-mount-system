from app.services import db
from app import model
import uuid


def get_events() -> list[model.Events]:
    with db.session.begin() as session:
        events = session.query(model.Events).all()
    return events


def get_event_by_id(event_id: uuid.UUID) -> model.Events | None:
    with db.session.begin() as session:
        event = session.query(model.Events).filter(model.Events.id == event_id).one_or_none()
    return event


def add_event(name: str) -> str:
    new_event = model.Events(name=name)
    with db.session.begin() as session:
        session.add(new_event)
        session.commit()
    return new_event.id
