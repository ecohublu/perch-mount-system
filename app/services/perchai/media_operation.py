import datetime
import uuid
from sqlalchemy.orm.session import Session

from app.services import db
import app.services.perchai.utils as services_utils
from app.error_handler import errors
from app import model


def add_uploaded_media(
    section_id: uuid.UUID,
    media: list[dict],
):
    if not media:
        raise errors.UploadMediaCanNotBeEmptyError()

    start_time = datetime.datetime(datetime.MAXYEAR, 1, 1, tzinfo=None)
    end_time = datetime.datetime(datetime.MINYEAR, 1, 1, tzinfo=None)
    model_media = []

    for medium in media:
        model_medium = model.Media(**medium)
        model_media.append(model_medium)
        start_time = min(model_medium.medium_datetime)
        end_time = max(model_medium.medium_datetime)

    _find_media_section_id(model_media, section_id)
    with db.session.begin() as session:
        try:
            session.query(model.Sections).filter(
                model.Sections.id == section_id
            ).update(
                {
                    "start_time": start_time,
                    "end_time": end_time,
                }
            )
            session.add_all(model_media)
            session.commit()
        except:
            session.rollback()
            raise
    return


def _find_media_section_id(media: list[model.Media], section_id: uuid.UUID):
    for medium in media:
        medium.section_id = section_id


def add_detected_media(
    detected_media: list[dict],
):
    media = [services_utils.DetectedMedium(**medium) for medium in detected_media]
    media = services_utils.DetectedMedia(media)
    detected_contents = [
        model.MediaDetectedContents(
            medium_id=medium.id,
            detected_at=medium.detected_at,
        )
        for medium in media
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
    with db.session.begin() as session:
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
            raise
    return


def add_checked_media(checked_media: list[dict]):
    media = [services_utils.CheckedMedium(**medium) for medium in checked_media]
    media = services_utils.CheckedMedia(media)
    unreviewed_media = [
        model.UnreviewedMediaContents(medium_id=medium.id)
        for medium in media.media_to_unreviewed
    ]
    accidental_media = [
        model.AccidentalMediaContents(medium_id=medium.id)
        for medium in media.media_to_accidenal
    ]
    with db.session.begin() as session:
        try:
            session.add_all(unreviewed_media)
            session.add_all(accidental_media)
            session.commit()
        except:
            session.rollback()
            raise


def add_reviewed_media(reviewed_media: list[dict]):
    media = [services_utils.ReviewedMedium(**medium) for medium in reviewed_media]
    media = services_utils.ReviewedMedia(media)
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

    with db.session.begin() as session:
        try:
            session.add_all(accidental_media)
            session.add_all(reviewed_media)
            _add_reviewed_insist_individuals(session, media)
            _add_reviewed_new_individuals(session, media)
            session.commit()
        except:
            session.rollback()
            raise


def _add_reviewed_new_individuals(
    session: Session,
    media: services_utils.ReviewedMedia,
):
    new_individuals = []
    new_reviewed_individuals = []
    new_marked_prey_individuals = []
    new_tagged_individuals = []
    for medium in media:
        medium: services_utils.ReviewedMedium = medium
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
    media: services_utils.ReviewedMedia,
):

    reviewed_individuals = []
    marked_prey_individuals = []
    tagged_individuals = []
    for medium in media:
        medium: services_utils.ReviewedMedium = medium
        for individual in medium.individuals:
            if individual.is_ai_detected:
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

    session.add_all(reviewed_individuals)
    session.add_all(marked_prey_individuals)
    session.add_all(tagged_individuals)
