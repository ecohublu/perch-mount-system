import flask
import flask_restful

from app.services import perchai as perchai_service


class Sections(flask_restful.Resource):
    def get(self):
        args = dict(flask.request.args)
        filter = perchai_service.utils.query_filter.SectionFilter(**args)
        sections = perchai_service.sections.get_sections(filter)
        return
