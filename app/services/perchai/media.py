import uuid
from sqlalchemy.orm.session import Session

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


def add_uploaded_media(
    uploaded_media: list[dict],
):
    media = [media_operator.UploadedMedia(**medium) for medium in uploaded_media]
    model_media = [
        model.Media(
            section_id=medium.section_id,
            medium_datetime=medium.medium_datetime,
            medium_type=medium.medium_type,
            nas_path=medium.nas_path,
        )
        for medium in media
    ]
    with perchai.session.begin() as session:
        try:
            session.add_all(model_media)
            session.flush()
            undetected_contents = [
                model.UndetectedMediaContents(medium_id=medium.id)
                for medium in model_media
            ]
            session.add_all(undetected_contents)
            session.commit()
        except:
            session.rollback()
    return


def add_detected_media(
    detected_media: list[dict],
):
    media = [media_operator.DetectedMedia(**medium) for medium in detected_media]
    detected_contents = [
        model.MediaDetectedContents(medium_id=medium.id) for medium in media
    ]
    unchecked_contents = [
        model.UncheckedMediaContents(medium_id=medium.id)
        for medium in media.media_to_unchecked
    ]
    unreviewed_contents: list[model.UnreviewedMediaContents] = []
    unreviewed_individuals: list[model.UnreviewedIndividualsContents] = []
    individuals: list[model.Individuals] = []
    for medium in media.media_to_unreviewed:
        unreviewed_contents.append(model.UnreviewedMediaContents(medium_id=medium.id))
        for individual in medium.individuals:
            individuals.append(model.Individuals(medium_id=medium.id))
            unreviewed_individuals.append(
                model.UnreviewedIndividualsContents(
                    taxon_order_by_ai=individual.taxon_order_by_ai,
                    box_xmin=individual.box_xmin,
                    box_xmax=individual.box_xmax,
                    box_ymin=individual.box_ymin,
                    box_ymax=individual.box_ymax,
                )
            )
    with perchai.session.begin() as session:
        try:
            session.add_all(individuals)
            session.flush()
            for i, individual in enumerate(individuals):
                unreviewed_individuals[i].individual_id = individual.id
            session.add_all(unreviewed_individuals)
            session.add_all(detected_contents)
            session.add_all(unchecked_contents)
            session.add_all(unreviewed_contents)
            session.commit()
        except:
            session.rollback()
    return


def add_checked_media(checked_media: list[dict]):
    media = [media_operator.CheckedMedia(**medium) for medium in checked_media]
    unreviewed_media = [
        model.UnreviewedMediaContents(medium_id=medium.id)
        for medium in media.media_to_unreviewed
    ]
    accidental_media = [
        model.AccidentalMediaContents(medium_id=medium.id)
        for medium in media.media_to_accidenal
    ]
    with perchai.session.begin() as session:
        try:
            session.add_all(unreviewed_media)
            session.add_all(accidental_media)
            session.commit()
        except:
            session.rollback()


def add_reviewed_media(reviewed_media: list[dict]):
    media = [media_operator.ReviewedMedia(**medium) for medium in reviewed_media]
    accidental_media = [
        model.AccidentalMediaContents(medium_id=medium.id)
        for medium in media.media_to_accidenal
    ]
    reviewed_media: list[model.ReviewedMediaContents] = []

    for medium in media.media_to_reviewed:
        reviewed_media.append(
            model.ReviewedMediaContents(
                medium_id=medium.id,
                reviewed_at=medium.reviewed_at,
                reviewer_id=medium.reviewer_id,
                fearured_by_id=medium.featured_by_id,
                event_id=medium.event_id,
                behavior_id=medium.behavior_id,
            )
        )

    with perchai.session.begin() as session:
        try:
            session.add_all(accidental_media)
            session.add_all(reviewed_media)
            _add_reviewed_insist_individuals(session, media)
            _add_reviewed_new_individuals(session, media)
            session.commit()
        except:
            session.rollback()


def _add_reviewed_new_individuals(
    session: Session,
    media: media_operator.ReviewedMedia,
):
    new_individuals = []
    new_reviewed_individuals = []
    new_marked_prey_individuals = []
    new_tagged_individuals = []
    for medium in media:
        medium: media_operator.ReviewedMedium = medium
        for individual in medium.individuals:
            if not individual.is_ai_detected:
                continue
            new_individuals.append(model.Individuals(medium_id=medium.id))
            new_reviewed_individuals.append(
                model.ReviewedIndividualsContents(
                    taxon_order_by_human=individual.taxon_order_by_human,
                    box_xmin=individual.box_xmin,
                    box_xmax=individual.box_xmax,
                    box_ymin=individual.box_ymin,
                    box_ymax=individual.box_ymax,
                )
            )
            new_marked_prey_individuals.append(
                model.MarkedPreyIndividualsContents(has_prey=individual.has_prey)
            )
            new_tagged_individuals.append(
                model.TaggedIndividualsContents(
                    is_tagged=individual.is_tagged,
                    has_ring=individual.has_ring,
                    ring_number=individual.ring_number,
                )
            )

    session.add_all(new_individuals)
    session.flush()
    for i, r, m, t in zip(
        new_individuals,
        new_reviewed_individuals,
        new_marked_prey_individuals,
        new_tagged_individuals,
    ):
        r.individual_id = i.id
        m.individual_id = i.id
        t.individual_id = i.id
    session.add_all(new_reviewed_individuals)
    session.add_all(new_marked_prey_individuals)
    session.add_all(new_tagged_individuals)


def _add_reviewed_insist_individuals(
    session: Session,
    media: media_operator.ReviewedMedia,
):
    individuals = []
    reviewed_individuals = []
    marked_prey_individuals = []
    tagged_individuals = []
    for medium in media:
        medium: media_operator.ReviewedMedium = medium
        for individual in medium.individuals:
            if individual.is_ai_detected:
                individuals.append(
                    model.Individuals(id=individual.id, medium_id=medium.id)
                )
                reviewed_individuals.append(
                    model.ReviewedIndividualsContents(
                        individual_id=individual.id,
                        taxon_order_by_human=individual.taxon_order_by_human,
                        box_xmin=individual.box_xmin,
                        box_xmax=individual.box_xmax,
                        box_ymin=individual.box_ymin,
                        box_ymax=individual.box_ymax,
                    )
                )
                marked_prey_individuals.append(
                    model.MarkedPreyIndividualsContents(
                        individual_id=individual.id, has_prey=individual.has_prey
                    )
                )
                tagged_individuals.append(
                    model.TaggedIndividualsContents(
                        individual_id=individual.id,
                        is_tagged=individual.is_tagged,
                        has_ring=individual.has_ring,
                        ring_number=individual.ring_number,
                    )
                )
    session.add_all(individuals)
    session.add_all(reviewed_individuals)
    session.add_all(marked_prey_individuals)
    session.add_all(tagged_individuals)
