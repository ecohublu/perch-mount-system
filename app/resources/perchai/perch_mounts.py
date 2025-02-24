import flask_restful
import uuid

from app.services import perchai as perchai_service
import app.resources.perchai.string_query_converters as sq_converters
import app.resources.utils as res_utils


class PerchMounts(flask_restful.Resource):
    @res_utils.parse_args(sq_converters.perch_mount)
    def get(self, parsed_args):
        filter = perchai_service.utils.query_filter.PerchMountFilter(**parsed_args)
        perch_mounts = perchai_service.perch_mounts.get_perch_mounts_by_filter(filter)
        return [perch_mount.to_dict() for perch_mount in perch_mounts]


class PerchMount(flask_restful.Resource):
    def get(self, perch_mount_id: uuid.UUID):
        perch_mount = perchai_service.perch_mounts.get_perch_mount_by_id(perch_mount_id)
        return perch_mount.to_dict()
