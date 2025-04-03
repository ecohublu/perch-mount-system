import uuid
import flask_jwt_extended
import flask_restx

from app.resources.data_export import parsers
import app.services.data_export.data as data_services
import app.services.perchai as perchai_service
import app.resources.utils as resource_utils


class Data(flask_restx.Resource):
    @resource_utils.parse_args(parsers.Previews.get)
    def get(self, parsed_args):
        data = data_services.get_data(**parsed_args, limit=100)
        return data.to_dict()


class EmailExports(flask_restx.Resource):
    @flask_jwt_extended.jwt_required()
    @resource_utils.parse_args(parsers.EmailExport.post)
    def post(self, parsed_args: dict):
        identity = flask_jwt_extended.get_jwt_identity()
        member = perchai_service.members.get_member_by_id(uuid.UUID(identity))
        mail_to = parsed_args["mail_to"] if "mail_to" in parsed_args else member.gmail
        parsed_args.pop("mail_to")
        data = data_services.get_data()

        return {"message": f"data sent to {mail_to} successfully."}
