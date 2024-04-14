import flask

import flask_jwt_extended

import service.export_history
from src import pm_resource


class ExportHistories(pm_resource.PerchMountResource):
    @flask_jwt_extended.jwt_required()
    def get(self):
        args = dict(flask.request.args)
        args = self._correct_types(args)
        histories = service.export_history.get_export_histories_by_exportor(**args)
        return {"export_histories": [history.to_json() for history in histories]}
