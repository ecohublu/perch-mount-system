import uuid

from app.services import db
import app.services.perchai.utils as services_utils
from app import model


def contribute(
    contribution_type: model.enums.ContributionType,
    contributor_id: uuid.UUID,
    counts: int,
):
    with db.session.begin() as session:
        new_contribution = model.Contributions(
            contribution_type=contribution_type,
            contributor_id=contributor_id,
            counts=counts,
        )
        session.add(new_contribution)
        session.commit()
    return


def get_contributions_by_filter(
    filter: services_utils.ContributionFilter,
) -> list[model.Contributions]:
    modifier = services_utils.ContributionsQueryModifier(filter)
    with db.session.begin() as session:
        query = session.query(model.Contributions)
        query = modifier.filter_query(query)
        contributions = query.all()
    return contributions
