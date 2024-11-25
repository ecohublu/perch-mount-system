import datetime
import service
from service import utils
from src import model


def get_empty_media(
    section_id: int = None,
    perch_mount_id: int = None,
    datetime_from: datetime.datetime = None,
    datetime_to: datetime.datetime = None,
    offset: int = 0,
    limit: int = 100,
    order_by_datetime: bool = True,
) -> list[model.EmptyMedia]:
    with service.session.begin() as session:
        query = session.query(
            model.EmptyMedia.empty_medium_id,
            model.EmptyMedia.section,
            model.EmptyMedia.medium_datetime,
            model.EmptyMedia.path,
            model.Sections.check_date,
            model.Sections.perch_mount,
            model.PerchMounts.perch_mount_name,
            model.Projects.name.label("project_name"),
        )

        query = query.filter(model.EmptyMedia.checked == False)

        if section_id:
            query = query.filter(model.EmptyMedia.section == section_id)

        if perch_mount_id:
            query = query.filter(model.Sections.perch_mount == perch_mount_id)

        if datetime_from:
            query = query.filter(model.EmptyMedia.medium_datetime >= datetime_from)

        if datetime_to:
            query = query.filter(model.EmptyMedia.medium_datetime < datetime_to)

        if order_by_datetime:
            query = query.order_by(model.EmptyMedia.medium_datetime)

        query = query.join(
            model.Sections,
            model.Sections.section_id == model.EmptyMedia.section,
        )
        query = query.join(
            model.PerchMounts,
            model.PerchMounts.perch_mount_id == model.Sections.perch_mount,
        )
        query = query.join(
            model.Projects,
            model.Projects.project_id == model.PerchMounts.project,
        )

        query = query.order_by(model.EmptyMedia.medium_datetime)
        query = query.offset(offset).limit(limit)
        results = query.all()
    return results


def get_empty_medium_by_id(empty_medium_id: str) -> model.EmptyMedia:
    with service.session.begin() as session:
        query = (
            session.query(
                model.EmptyMedia.empty_medium_id,
                model.EmptyMedia.section,
                model.EmptyMedia.medium_datetime,
                model.EmptyMedia.path,
                model.Sections.check_date,
                model.Sections.perch_mount,
                model.PerchMounts.perch_mount_name,
                model.Projects.name.label("project_name"),
            )
            .filter(model.EmptyMedia.empty_medium_id == empty_medium_id)
            .filter(model.EmptyMedia.checked == False)
        )
        query = query.join(
            model.Sections,
            model.Sections.section_id == model.EmptyMedia.section,
        )
        query = query.join(
            model.PerchMounts,
            model.PerchMounts.perch_mount_id == model.Sections.perch_mount,
        )
        query = query.join(
            model.Projects,
            model.Projects.project_id == model.PerchMounts.project,
        )
        result = query.one_or_none()
    return result


def add_empty_media(empty_media: list[dict]):
    new_media = [model.EmptyMedia(**medium) for medium in empty_media]
    with service.session.begin() as session:
        session.add_all(new_media)
        session.commit()


def checked_empty_media(medium_indice: list[str]):
    with service.session.begin() as session:
        session.query(model.EmptyMedia).filter(
            model.EmptyMedia.empty_medium_id.in_(medium_indice)
        ).update()
        session.commit()


def delete_checked_empty_media():
    with service.session.begin() as session:
        session.query(model.EmptyMedia).filter(
            model.EmptyMedia.checked == True
        ).delete()
        session.commit()


def empty_check(media: list[dict], empty_checker_id: int):
    all_indice = [medium["empty_medium_id"] for medium in media]
    new_media = []
    empty_paths = []

    for medium in media:
        if medium["empty"]:
            empty_paths.append(utils.get_delete_medium(medium))
            continue
        new_media.append(
            model.DetectedMedia(
                detected_medium_id=medium["empty_medium_id"],
                medium_datetime=medium["medium_datetime"],
                section=medium["section"],
                empty_checker=medium["empty_checker"],
                path=medium["path"],
            )
        )

    contribution = model.Contributions(
        contributor=empty_checker_id,
        num_files=len(media),
        action=1,
    )

    with service.session.begin() as session:
        try:
            session.query(model.EmptyMedia).filter(
                model.EmptyMedia.empty_medium_id.in_(all_indice)
            ).update({"checked": True})
            session.add_all(new_media)

            if empty_paths:
                utils.post_delete_media_task(empty_paths)

            session.add(contribution)
            session.commit()
        except Exception as e:
            session.rollback()
            raise SystemError(e)
