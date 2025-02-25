import flask_restful
import uuid

from app.services import perchai as perchai_service


class Members(flask_restful.Resource):
    def get(self):
        members = perchai_service.members.get_members()
        return [member.to_dict() for member in members]


class Member(flask_restful.Resource):
    def get(self, perch_mount_id: uuid.UUID):
        member = perchai_service.members.get_member_by_id(perch_mount_id)
        return member.to_dict()
