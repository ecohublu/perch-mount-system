import uuid

from app.services import perchai
from app.services.perchai.utils import query_filter, query_modifier, media_operator
from app import model


def get_media(filter: query_filter.MediaFilter) -> list[model.Media]:
    modifier = query_modifier.MediaQueryModifier(filter)
    with perchai.session.begin() as session:
        query = session.query(model.Media)
        query = modifier.options(query)
        query = modifier.filter_query(query)
        query = modifier.limit_query(query)
        query = modifier.offset_query(query)
        media = query.all()
    return media


def get_medium_by_id(medium_id: str) -> model.Media:
    medium_id = uuid.UUID(medium_id)
    with perchai.session.begin() as session:
        query = session.query(model.Media).filter(model.Media.id == medium_id)
        medium = query.one_or_none()

    return medium


def add_uploaded_media(media: list[media_operator.UploadedMedium]):
    return


def add_detected_media(media: list[media_operator.DetectedMedium]):
    return


def add_checked_media(media: list[media_operator.CheckedMedium]):
    return


def add_reviewed_media(media: list[media_operator.ReviewedMedium]):
    return


def add_media_and_individuals(media: list[dict]):
    individauls = _get_individauls_from_media(media)
    media = _pop_media_individual(media)
    new_meida: list[model.Media] = []
    new_individuals: list[model.Individuals] = []
    for medium in media:
        new_meida.append(model.Media(**medium))
    for individual in individauls:
        new_individuals.append(model.Individuals(**individual))

    with perchai.session.begin() as session:
        try:
            session.add_all(new_meida)
            session.flush()
            session.add_all(new_individuals)
            session.commit()
        except:
            session.rollback()
            raise


def _get_individauls_from_media(media: list[dict]) -> list[dict]:
    individuals = []
    for medium in media:
        for individual in medium["individuals"]:
            individual["medium"] = medium["medium_id"]
            individuals.append(individual)
    return individuals


def _pop_media_individual(media: list[dict]) -> list[dict]:
    for medium in media:
        medium.pop("individuals")
    return media
