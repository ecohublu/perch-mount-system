import uuid
import flask_jwt_extended
import flask_restx

from app.resources.data_export import parsers
from app.resources.data_export import csv
import app.services.data_export.data as data_services
import app.services.perchai as perchai_service
import app.resources.utils as resource_utils
from app.resources.data_export import marshals


class Data(flask_restx.Resource):
    @resource_utils.parse_args(parsers.Previews.get)
    @flask_restx.marshal_with(marshals.data_model)
    def get(self, parsed_args):
        helper = data_services.DataExportQueryHelper(**parsed_args)
        data = data_services.get_data(helper, limit=100)

        return [row._asdict() for row in data]


class EmailExports(flask_restx.Resource):
    @flask_jwt_extended.jwt_required()
    @resource_utils.parse_args(parsers.EmailExport.post)
    @flask_restx.marshal_with(marshals.data_model)
    def post(self, parsed_args: dict):
        identity = flask_jwt_extended.get_jwt_identity()
        member = perchai_service.members.get_member_by_id(uuid.UUID(identity))

        mail_to = parsed_args["mail_to"] if "mail_to" in parsed_args else member.gmail
        parsed_args.pop("mail_to")

        helper = data_services.DataExportQueryHelper(**parsed_args)
        data = data_services.get_data(helper)
        csv_data = csv.json_to_csv([row._asdict() for row in data])

        # TODO send email
        print(csv_data)

        return {"message": f"data sent to {mail_to} successfully."}
