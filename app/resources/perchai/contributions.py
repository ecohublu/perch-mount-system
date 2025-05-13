import flask_restx
import uuid

from app.services import perchai as perchai_service
import app.resources.perchai.utils as perchai_utils
from app.resources.perchai import parsers
import app.resources.utils as resource_utils


class Contributions(flask_restx.Resource):
    @resource_utils.parse_args(parsers.Contributions.get)
    def get(self, parsed_args):
        filter = perchai_service.utils.query_filter.ContributionFilter(**parsed_args)
        contributions = perchai_service.contributions.get_contributions_by_filter(
            filter
        )
        return [contribution.to_dict() for contribution in contributions]


class MemberContributions(flask_restx.Resource):
    @resource_utils.parse_args(parsers.MemberContributions.get)
    def get(self, member_id: uuid.UUID, parsed_args):

        filter = perchai_service.utils.query_filter.ContributionFilter(
            member_id, **parsed_args
        )
        contributions = perchai_service.contributions.get_contributions_by_filter(
            filter
        )
        return [contribution.to_dict() for contribution in contributions]
