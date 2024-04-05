import flask
import summary.service.data_export
from summary.filer import csv
from src import pm_resource


class ExportData(pm_resource.PerchMountResource):
    def get(self):
        args = flask.request.args
        args = self._correct_types(args)
        results = summary.service.data_export.get_export_data(**args)
        csv.query_result_to_csv(results)
        return {"message": "successed"}
