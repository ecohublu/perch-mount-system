import uuid

from app.services import db
import app.services.perchai.utils as services_utils
from app import model


def get_media_by_filter(filter: services_utils.MediaFilter) -> list[model.Media]:
    modifier = services_utils.MediaQueryModifier(filter)
    with db.session.begin() as session:
        query = session.query(model.Media)
        query = modifier.options(query)
        query = modifier.filter_query(query)
        query = modifier.limit_query(query)
        query = modifier.offset_query(query)
        media = query.all()
    return media


def get_medium_by_id(medium_id: uuid.UUID) -> model.Media | None:
    with db.session.begin() as session:
        query = session.query(model.Media).filter(model.Media.id == medium_id)
        medium = query.one_or_none()

    return medium


def update_media_feature(medium_id: uuid.UUID, args: dict):
    with db.session.begin() as session:
        session.query(model.ReviewedMediaContents).filter(
            model.ReviewedMediaContents.medium_id == medium_id
        ).update(args)
        session.commit()
