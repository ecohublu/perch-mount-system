from datetime import date
import uuid

from app.services import perchai
from app.services.perchai.utils import query_filter, query_modifier
from app import model


def get_sections(filter: query_filter.SectionFilter) -> list[model.Sections]:
    modifier = query_modifier.SectionQueryModifier(filter)
    with perchai.session.begin() as session:
        query = session.query(model.Sections)
        query = modifier.filter_query(query)
        sections = query.all()
    return sections


def get_section_by_id(section_id: str) -> model.Sections:
    uuid.UUID(section_id)
    with perchai.session.begin() as session:
        section = (
            session.query(model.Sections).filter(model.Sections.id == section_id).one()
        )
    return section


def add_section(
    perch_mount_id: str,
    mount_type_id: str,
    camera_id: str,
    swapper_date: date,
    swapper_ids: list[str],
    valid: bool,
    note: str | None = None,
) -> int:
    perch_mount_id = uuid.UUID(perch_mount_id)
    mount_type_id = uuid.UUID(mount_type_id)
    camera_id = uuid.UUID(camera_id)
    swapper_ids = list(map(uuid.UUID, swapper_ids))

    new_section = model.Sections(
        perch_mount_id=perch_mount_id,
        mount_type=mount_type_id,
        camera=camera_id,
        swapper_date=swapper_date,
        swapper_ids=swapper_ids,
        valid=valid,
        note=note,
    )

    with perchai.session.begin() as session:
        session.add(new_section)
        session.commit()
        new_id = new_section.id

    return new_id
