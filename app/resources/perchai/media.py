import flask_restx
import uuid

from app.services import perchai as perchai_service
from app.resources.perchai import parsers
import app.resources.utils as resource_utils
from app.error_handler import errors
from app import model


class Media(flask_restx.Resource):
    @resource_utils.parse_args(parsers.Media.get)
    def get(self, parsed_args):
        filter = perchai_service.utils.query_filter.MediaFilter(**parsed_args)
        media = perchai_service.media.get_media_by_filter(filter)
        return [medium.to_dict() for medium in media]


class Medium(flask_restx.Resource):
    def get(self, medium_id: uuid.UUID):
        medium = perchai_service.media.get_medium_by_id(medium_id)

        if medium is None:
            raise errors.ResourceNotFoundError(model.Media.__name__)

        return medium.to_dict()

class MediumFeature(flask_restx.Resource):
    def patch(self, medium_id: uuid.UUID, parsed_args: dict):
        perchai_service.media.update_media_feature(medium_id, parsed_args)
        medium = perchai_service.media.get_medium_by_id(medium_id)
        return medium.to_dict()

class UploadedMedia(flask_restx.Resource):
    @resource_utils.parse_json_body_args(parsers.UploadedMedia.post)
    def post(self, media):
        perchai_service.media_operation.add_uploaded_media(**media)


class DetectedMedia(flask_restx.Resource):
    @resource_utils.parse_json_body_args(parsers.DetectedMedia.post)
    def post(self, media):
        perchai_service.media_operation.add_detected_media(media)


class CheckedMedia(flask_restx.Resource):
    @resource_utils.parse_json_body_args(parsers.CheckedMedia.post)
    def post(self, media):
        perchai_service.media_operation.add_checked_media(media)


class ReviewedMedia(flask_restx.Resource):
    @resource_utils.parse_json_body_args(parsers.ReviewedMedia.post)
    def post(self, media):
        perchai_service.media_operation.add_reviewed_media(media)
