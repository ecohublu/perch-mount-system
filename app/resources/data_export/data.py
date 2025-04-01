import flask_jwt_extended
import flask_restx

from app.resources.data_export import parsers
import app.resources.utils as resource_utils


class Data(flask_restx.Resource):
    @resource_utils.parse_args(parsers.Previews.get)
    def get(self, parsed_args: dict):
        return


class EmailExports(flask_restx.Resource):
    @flask_jwt_extended.jwt_required()
    @resource_utils.parse_args(parsers.EmailExport.post)
    def post(self, parsed_args: dict):
        return
