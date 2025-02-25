import flask_restful
import uuid

from app.services import perchai as perchai_service
import app.resources.perchai.string_query_converters as sq_converters
import app.resources.utils as res_utils
from app.error_handler import errors

class Media(flask_restful.Resource):
    @res_utils.parse_args(sq_converters.media)
    def get(self, parsed_args):

        STATUS_FIELD = "status"
        if STATUS_FIELD not in parsed_args:
            raise errors.StringQueryMissingError(STATUS_FIELD)

        filter = perchai_service.utils.query_filter.MediaFilter(**parsed_args)
        media = perchai_service.media.get_media_by_filter(filter)
        return [medium.to_dict() for medium in media]


class Medium(flask_restful.Resource):
    def get(self, medium_id: uuid.UUID):
        medium = perchai_service.media.get_medium_by_id(medium_id)
        print(type(medium_id))
        if medium is None:
            raise errors.ResourceNotFoundError(type(medium).__name__)

        return medium.to_dict()
