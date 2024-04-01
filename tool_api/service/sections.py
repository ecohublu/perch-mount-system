import datetime
import sqlalchemy

import service
from service import sections
from src import model


_SHIFT_SECTION_TIME_EXPRESSION = """
UPDATE
    perch_mount.sections
SET
    start_time = ADDDATE(start_time, INTERVAL %s MINUTE),
    end_time = ADDDATE(end_time, INTERVAL %s MINUTE)
WHERE
    section_id = %s;
"""

_SHIFT_MEIDA_TIME_EXPRESSION = """
UPDATE
    perch_mount.%s
SET
    medium_datetime = ADDDATE(medium_datetime, INTERVAL %s MINUTE)
WHERE
    section = %s;
"""


def shift_datetimes(section_id: int = None, new_start_time: datetime.datetime = None):
    section = sections.get_section_by_id(section_id)
    time_diff: datetime.timedelta = new_start_time - section.start_time
    minutes = time_diff.total_seconds() // 60

    section_sql = _get_shift_section_time_expression(section_id, minutes)
    empty_media_sql = _get_shift_media_time_expression(
        "empty_media",
        section_id,
        minutes,
    )
    detected_media_sql = _get_shift_media_time_expression(
        "detected_media",
        section_id,
        minutes,
    )
    media_sql = _get_shift_media_time_expression(
        "media",
        section_id,
        minutes,
    )

    with service.session.begin() as session:
        try:
            session.execute(sqlalchemy.text(section_sql))
            session.execute(sqlalchemy.text(empty_media_sql))
            session.execute(sqlalchemy.text(detected_media_sql))
            session.execute(sqlalchemy.text(media_sql))
            session.commit()
        except Exception as e:
            print(e)
            session.rollback()


def _get_shift_section_time_expression(section_id: int, minutes: int) -> str:
    return _SHIFT_SECTION_TIME_EXPRESSION % (minutes, minutes, section_id)


def _get_shift_media_time_expression(
    table_name: str, section_id: int, minutes: int
) -> str:
    return _SHIFT_MEIDA_TIME_EXPRESSION % (table_name, minutes, section_id)
