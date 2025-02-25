from app.services import perchai
from app import model
import uuid


def get_events() -> list[model.Events]:
    with perchai.session.begin() as session:
        events = session.query(model.Events).all()
    return events


def get_event_by_id(event_id: str) -> model.Events | None:
    event_id = uuid.UUID(event_id)
    with perchai.session.begin() as session:
        event = session.query(model.Events).filter(model.Events.id == event_id).one()
    return event


def add_event(name: str) -> str:
    new_event = model.Events(name=name)
    with perchai.session.begin() as session:
        session.add(new_event)
        session.commit()
    return new_event.id
