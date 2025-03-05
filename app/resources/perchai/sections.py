import flask_restx
import uuid

from app.services import perchai as perchai_service
from app.resources.perchai import parsers
import app.resources.utils as resource_utils
from app.error_handler import errors
from app import model


class Sections(flask_restx.Resource):
    @resource_utils.parse_args(parsers.Sections.get)
    def get(self, parsed_args):
        filter = perchai_service.utils.query_filter.SectionFilter(**parsed_args)
        sections = perchai_service.sections.get_sections_by_filter(filter)
        return [section.to_dict() for section in sections]

    def post(self):
        return


class Section(flask_restx.Resource):
    def get(self, section_id: uuid.UUID):
        section = perchai_service.sections.get_section_by_id(section_id)

        if section is None:
            raise errors.ResourceNotFoundError(model.Sections.__name__)

        return section.to_dict()
