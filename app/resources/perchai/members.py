import flask_restx
import uuid

from app.resources.perchai import parsers
import app.services.perchai as perchai_service
import app.resources.perchai.utils as perchai_utils
import app.resources.utils as resource_utils
from app.error_handler import errors
from app import model


class Members(flask_restx.Resource):
    def get(self):
        members = perchai_service.members.get_members()
        return [member.to_dict() for member in members]

    @resource_utils.parse_args(parsers.Members.post)
    def post(self, parsed_args):
        new_member_id = perchai_service.members.add_member(**parsed_args)
        return perchai_utils.id_json(new_member_id)


class Member(flask_restx.Resource):
    def get(self, perch_mount_id: uuid.UUID):
        member = perchai_service.members.get_member_by_id(perch_mount_id)

        if member is None:
            raise errors.ResourceNotFoundError(model.Members.__name__)

        return member.to_dict()

    @resource_utils.parse_json_body_args(parsers.Member.post)
    def post(self, member_id: uuid.UUID, parsed_args: dict):
        perchai_service.members.update_member(member_id, parsed_args)
        member = perchai_service.members.get_member_by_id(member_id)
        return member.to_dict()


class MemberBlock(flask_restx.Resource):
    def post(self, member_id: uuid.UUID):
        perchai_service.members.block_member(member_id)
        member = perchai_service.members.get_member_by_id(member_id)
        return member.to_dict()

    def delete(self, member_id: uuid.UUID):
        member = perchai_service.members.get_member_by_id(member_id)
        perchai_service.members.unblock_member(member_id)
        return member.to_dict()


class MemberActivation(flask_restx.Resource):
    def post(self, member_id: uuid.UUID):
        member = perchai_service.members.get_member_by_id(member_id)
        perchai_service.members.activate_member(member_id)
        return member.to_dict()

    def delete(self, member_id: uuid.UUID):
        perchai_service.members.deactivate_member(member_id)
        member = perchai_service.members.get_member_by_id(member_id)
        return member.to_dict()
