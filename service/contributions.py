import datetime
import service
from src import model


def get_contributions(
    date_from: datetime.date = None,
    date_to: datetime.date = None,
    contributor_id: int = None,
    action_id: int = None,
) -> list[model.Contributions]:
    with service.session.begin() as session:
        query = session.query(
            model.Contributions.action,
            model.Contributions.num_files,
            model.Contributions.time,
            model.Contributions.contributor,
            model.Members.user_name,
            model.Actions.name,
        )
        if date_from:
            query = query.filter(model.Contributions.time >= date_from)
        if date_to:
            query = query.filter(model.Contributions.time < date_to)
        if contributor_id:
            query = query.filter(model.Contributions.contribution_id == contributor_id)
        if action_id:
            query = query.filter(model.Contributions.action == action_id)

        query = query.join(
            model.Members,
            model.Members.member_id == model.Contributions.contributor,
        )

        query = query.join(
            model.Actions,
            model.Actions.action_id == model.Actions.action_id,
        )
        query = query.order_by(model.Contributions.time)

    return query.all()


def contribute(
    contributor_id: int,
    num_files: int,
    action: int,
) -> int:
    new_contribution = model.Contributions(
        contributor=contributor_id,
        num_files=num_files,
        action=action,
    )
    with service.session.begin() as session:
        session.add(new_contribution)
        session.commit()
    return new_contribution.contribution_id
