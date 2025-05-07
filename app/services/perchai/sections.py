from datetime import date
import sqlalchemy
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
        query = query.order_by(model.Sections.swapped_date.desc())
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
        mount_type_id=mount_type_id,
        camera_id=camera_id,
        swapped_date=swapped_date,
        valid=valid,
        note=note,
    )

    with db.session.begin() as session:
        try:
            session.add(new_section)
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


def delete_section(section_id: uuid.UUID):
    stmt = sqlalchemy.delete(model.sections_swappers).where(
        model.sections_swappers.c.section_id == section_id
    )
    with db.session.begin() as session:
        try:
            session.execute(stmt)
            session.query(model.Sections).filter(
                model.Sections.id == section_id
            ).delete()
            session.commit()
        except:
            session.rollback()
            raise


def update_section_swappers_by_id(
    section_id: uuid.UUID,
    swapper_ids: list[uuid.UUID],
):
    delete_stmt = sqlalchemy.delete(model.sections_swappers).where(
        model.sections_swappers.c.section_id == section_id
    )
    insert_stmt = sqlalchemy.insert(model.sections_swappers)
    insert_data = [
        {
            "section_id": section_id,
            "swapper_id": swapper_id,
        }
        for swapper_id in swapper_ids
    ]

    with db.session.begin() as session:
        try:
            session.execute(delete_stmt)
            session.execute(insert_stmt, insert_data)
        except:
            session.rollback()
            raise
    return
