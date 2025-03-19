import flask_restx
import uuid

from app.services import perchai as perchai_service
from app.resources.perchai import parsers
import app.resources.perchai.utils as perchai_utils
import app.resources.utils as resource_utils
from app.error_handler import errors
from app import model


class PerchMounts(flask_restx.Resource):
    @resource_utils.parse_args(parsers.PerchMounts.get)
    def get(self, parsed_args):
        filter = perchai_service.utils.query_filter.PerchMountFilter(**parsed_args)
        perch_mounts = perchai_service.perch_mounts.get_perch_mounts_by_filter(filter)
        return [perch_mount.to_dict() for perch_mount in perch_mounts]

    @resource_utils.parse_args(parsers.PerchMounts.post)
    def post(self, parsed_args):
        new_perch_mount_id = perchai_service.perch_mounts.add_perch_mount(**parsed_args)
        return perchai_utils.id_json(new_perch_mount_id)


class PerchMount(flask_restx.Resource):
    def get(self, perch_mount_id: uuid.UUID):
        perch_mount = perchai_service.perch_mounts.get_perch_mount_by_id(perch_mount_id)

        if perch_mount is None:
            raise errors.ResourceNotFoundError(model.PerchMounts.__name__)

        return perch_mount.to_dict()

    def patch(self, perch_mount_id: uuid.UUID):
        return
