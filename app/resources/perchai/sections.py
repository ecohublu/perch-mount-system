import flask_restx
import uuid

from app.services import perchai as perchai_service
from app.resources.perchai import parsers
import app.resources.utils as resource_utils
import app.resources.perchai.utils as perchai_utils
from app.error_handler import errors
from app import model


class Sections(flask_restx.Resource):
    @resource_utils.parse_args(parsers.Sections.get)
    def get(self, parsed_args):
        filter = perchai_service.utils.query_filter.SectionFilter(**parsed_args)
        sections = perchai_service.sections.get_sections_by_filter(filter)
        return [section.to_dict() for section in sections]

    @resource_utils.parse_args(parsers.Sections.post)
    def post(self, parsed_args):
        new_section = perchai_service.sections.add_section(**parsed_args)
        return new_section.to_dict()


class Section(flask_restx.Resource):
    def get(self, section_id: uuid.UUID):
        section = perchai_service.sections.get_section_by_id(section_id)

        if section is None:
            raise errors.ResourceNotFoundError(model.Sections.__name__)

        return section.to_dict()

    @resource_utils.parse_json_body_args(parsers.Section.patch)
    def patch(self, section_id: uuid.UUID, parsed_args):
        perchai_service.sections.update_section(section_id, parsed_args)
        section = perchai_service.sections.get_section_by_id(section_id)
        return section.to_dict()
