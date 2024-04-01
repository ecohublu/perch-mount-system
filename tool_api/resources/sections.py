import flask
import flask_jwt_extended

import tool_api.service.sections
import service.sections
from src import pm_resource


class TimeShifter(pm_resource.PerchMountResource):
    @flask_jwt_extended.jwt_required()
    def patch(self):
        args = dict(flask.request.args)
        args = self._correct_types(args)
        tool_api.service.sections.shift_datetimes(**args)
        section = service.sections.get_section_by_id(args["section_id"]).to_json()
        return {
            "new_start_time": section["start_time"],
            "new_end_time": section["end_time"],
        }
