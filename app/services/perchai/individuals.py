import uuid

from app.services import perchai
import app.services.perchai.utils as services_utils
from app import model
from app.error_handler import errors


def update_individual(individual_id: uuid.UUID, args: dict) -> model.Individuals | None:
    with perchai.session.begin() as session:
        individual = (
            session.query(model.Individuals.medium_id)
            .filter(model.Individuals.id == individual_id)
            .one_or_none()
        )

        if not individual:
            return None

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

            individual = (
                session.query(model.Individuals)
                .filter(model.Individuals.id == individual_id)
                .one()
            )
            session.commit()
        except:
            session.rollback()
            raise

    return individual
