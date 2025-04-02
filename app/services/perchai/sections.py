from datetime import date
import uuid

from app.services import db
import app.services.perchai.utils as services_utils
from app import model


def get_sections_by_filter(
    filter: services_utils.SectionFilter,
) -> list[model.Sections]:
    modifier = services_utils.SectionQueryModifier(filter)
    with db.session.begin() as session:
        query = session.query(model.Sections)
        query = modifier.filter_query(query)
        sections = query.all()
    return sections


def get_section_by_id(section_id: uuid.UUID) -> model.Sections | None:
    with db.session.begin() as session:
        section = (
            session.query(model.Sections)
            .filter(model.Sections.id == section_id)
            .one_or_none()
        )
    return section


def add_section(
    perch_mount_id: uuid.UUID,
    mount_type_id: uuid.UUID,
    camera_id: uuid.UUID,
    swapped_date: date,
    swapper_ids: list[uuid.UUID],
    valid: bool,
    note: str | None = None,
) -> model.Sections:

    new_section = model.Sections(
        perch_mount_id=perch_mount_id,
        mount_type=mount_type_id,
        camera=camera_id,
        swapped_date=swapped_date,
        swapper_ids=swapper_ids,
        valid=valid,
        note=note,
    )

    with db.session.begin() as session:
        try:
            session.add(section)
            session.flush()
            for swapper_id in swapper_ids:
                stat = model.sections_swappers.insert().values(
                    section_id=new_section.id, swapper_id=swapper_id
                )
                session.execute(stat)

            session.commit()
        except:
            session.rollback()
            raise

    with db.session.begin() as session:
        section = (
            session.query(model.Sections)
            .filter(model.Sections.id == new_section.id)
            .one()
        )

    return section


def update_section(section_id: uuid.UUID, arg: dict):
    with db.session.begin() as session:
        session.query(model.Sections).filter(model.Sections.id == section_id).update(
            arg
        )
        session.commit()
