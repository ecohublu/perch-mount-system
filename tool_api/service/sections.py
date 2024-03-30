import datetime


import service
from service import sections
from src import model


def shift_datetimes(section_id: int, new_start_time: datetime.datetime):
    section = sections.get_section_by_id(section_id)
    time_diff = new_start_time - section.start_time
    with service.session.begin() as session:
        try:
            session.query(model.Sections).filter(
                model.Sections.section_id == section_id
            ).update(
                {
                    "start_time": model.Sections.start_time + time_diff,
                    "end_time": model.Sections.end_time + time_diff,
                }
            )

            session.query(model.EmptyMedia).filter(
                model.EmptyMedia.section == section_id
            ).update({"medium_datetime": model.EmptyMedia.medium_datetime + time_diff})

            session.query(model.DetectedMedia).filter(
                model.DetectedMedia.section == section_id
            ).update(
                {"medium_datetime": model.DetectedMedia.medium_datetime + time_diff}
            )

            session.query(model.Media).filter(model.Media.section == section_id).update(
                {"medium_datetime": model.Media.medium_datetime + time_diff}
            )

            session.commit()
        except:
            session.rollback()
