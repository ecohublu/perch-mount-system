from datetime import date, datetime
import uuid

from app.services import perchai
import app.services.perchai.utils as services_utils
from app import model


def get_sections(filter: services_utils.SectionFilter) -> list[model.Sections]:
    modifier = services_utils.SectionQueryModifier(filter)
    with perchai.session.begin() as session:
        query = session.query(model.Sections)
        query = modifier.filter_query(query)
        sections = query.all()
    return sections


def get_section_by_id(section_id: uuid.UUID) -> model.Sections | None:
    with perchai.session.begin() as session:
        section = (
            session.query(model.Sections).filter(model.Sections.id == section_id).one()
        )
    return section


def add_section(
    perch_mount_id: str,
    mount_type_id: str,
    camera_id: str,
    swapped_date: date,
    start_time: str,
    end_time: str,
    swapper_ids: list[str],
    valid: bool,
    note: str | None = None,
) -> int:
    perch_mount_id = uuid.UUID(perch_mount_id)
    mount_type_id = uuid.UUID(mount_type_id)
    camera_id = uuid.UUID(camera_id)
    swapped_date = date.fromisoformat(swapped_date)
    start_time = datetime.fromisoformat(start_time)
    end_time = datetime.fromisoformat(end_time)
    swapper_ids = list(map(uuid.UUID, swapper_ids))

    new_section = model.Sections(
        perch_mount_id=perch_mount_id,
        mount_type=mount_type_id,
        camera=camera_id,
        swapped_date=swapped_date,
        swapper_ids=swapper_ids,
        valid=valid,
        note=note,
    )

    with perchai.session.begin() as session:
        session.add(new_section)
        session.commit()
        new_id = new_section.id

    return new_id
