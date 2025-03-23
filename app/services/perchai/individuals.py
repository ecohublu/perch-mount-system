import uuid

from app.services import perchai
import app.services.perchai.utils as services_utils
from app import model
from app.error_handler import errors


def get_individual_by_id(individual_id: uuid.UUID) -> model.Individuals | None:
    with perchai.session.begin() as session:
        individual = (
            session.query(model.Individuals)
            .filter(model.Individuals.id == individual_id)
            .one_or_none()
        )
    return individual


def update_individual(individual_id: uuid.UUID, args: dict):
    with perchai.session.begin() as session:
        individual = (
            session.query(model.Individuals.medium_id)
            .filter(model.Individuals.id == individual_id)
            .one_or_none()
        )

        if not individual:
            raise errors.ResourceNotFoundError(model.Individuals.__name__)

        medium = (
            session.query(model.Media.status)
            .filter(model.Media.id == individual.medium_id)
            .one()
        )

        if medium.status != model.enums.MediaStatus.REVIEWED:
            raise errors.StatusError(medium.status)

        try:
            session.query(model.ReviewedIndividualsContents).filter(
                model.ReviewedIndividualsContents.individual_id == individual_id
            ).update(args)

            session.commit()
        except:
            session.rollback()
            raise


def add_prey(
    individual_id: uuid.UUID,
    args: dict,
):
    with perchai.session.begin() as session:
        individual = (
            session.query(model.Individuals.prey_status)
            .filter(model.Individuals.id == individual_id)
            .one_or_none()
        )

        if not individual:
            raise errors.ResourceNotFoundError(model.Individuals.__name__)

        if individual.prey_status != model.enums.PreyStatus.NO_PREY:
            raise errors.StatusError(individual.prey_status)

        new_prey = model.IdentifiedPreyIndividualsContents(**args)
        new_prey.individual_id = individual_id

        try:
            session.query(model.MarkedPreyIndividualsContents).filter(
                model.MarkedPreyIndividualsContents.individual_id == individual_id
            ).update({"has_prey": True})
            session.add(new_prey)
            session.commit()
        except:
            session.rollback()
            raise


def update_prey(
    individual_id: uuid.UUID,
    args: dict,
):
    with perchai.session.begin() as session:
        individual = (
            session.query(model.Individuals.prey_status)
            .filter(model.Individuals.id == individual_id)
            .one_or_none()
        )

        if not individual:
            raise errors.ResourceNotFoundError(model.Individuals.__name__)

        if individual.prey_status != model.enums.PreyStatus.IDENTIFIED:
            raise errors.StatusError(individual.prey_status)

        try:
            session.query(model.IdentifiedPreyIndividualsContents).filter(
                model.IdentifiedPreyIndividualsContents.individual_id == individual_id
            ).update(args)
            session.commit()
        except:
            session.rollback()
            raise


def delete_prey(individual_id: uuid.UUID):
    with perchai.session.begin() as session:
        individual = (
            session.query(model.Individuals.prey_status)
            .filter(model.Individuals.id == individual_id)
            .one_or_none()
        )

        if not individual:
            raise errors.ResourceNotFoundError(model.Individuals.__name__)

        if individual.prey_status != model.enums.PreyStatus.IDENTIFIED:
            raise errors.StatusError(individual.prey_status)

        try:
            session.query(model.MarkedPreyIndividualsContents).filter(
                model.MarkedPreyIndividualsContents.individual_id == individual_id
            ).update({"has_prey": False})
            session.query(model.IdentifiedPreyIndividualsContents).filter(
                model.IdentifiedPreyIndividualsContents.individual_id == individual_id
            ).delete(synchronize_session=False)
            session.commit()
        except:
            session.rollback()
            raise


def upsert_note(individual_id: uuid.UUID, note: str):
    with perchai.session.begin() as session:
        individual = (
            session.query(model.Individuals)
            .filter(model.Individuals.id == individual_id)
            .one_or_none()
        )

        if not individual:
            raise errors.ResourceNotFoundError(model.Individuals.__name__)

        try:
            session.query(model.Individuals).filter(
                model.Individuals.id == individual_id
            ).update({"note": note})
            session.commit()
        except:
            session.rollback()
            raise


def remove_note(individual_id: uuid.UUID):
    with perchai.session.begin() as session:
        individual = (
            session.query(model.Individuals)
            .filter(model.Individuals.id == individual_id)
            .one_or_none()
        )

        if not individual:
            raise errors.ResourceNotFoundError(model.Individuals.__name__)

        try:
            session.query(model.Individuals).filter(
                model.Individuals.id == individual_id
            ).update({"note": None})
            session.commit()
        except:
            session.rollback()
            raise


def add_identified_preys(identified_preys: list[dict]):
    identified_preys = [
        model.IdentifiedPreyIndividualsContents(**prey) for prey in identified_preys
    ]
    with perchai.session.begin() as session:
        try:
            session.add_all(identified_preys)
            session.commit()
        except:
            session.rollback()
            raise
