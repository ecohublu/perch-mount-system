import csv
import flask
import io
import summary.service.data_export
import service.export_history
import summary.filer.csv
import io
from src import s3
from src import pm_resource
from src import config

PART_SIZE = 5 * 1024 * 1024


class ExportData(pm_resource.PerchMountResource):
    def get(self):
        args = flask.request.args
        args = self._correct_types(args)
        results = summary.service.data_export.get_export_data(**args)
        data = summary.filer.csv.PerchMountCsvData(results)
        # f = self._to_bytes_io(data)
        # self._save_to_minio(data.file_name, f)
        print(data.to_csv())
        return {"message": "successed"}

    def _to_bytes_io(self, data: str) -> io.BytesIO:
        f = io.BytesIO()
        f.write(bytes(data))
        f.seek(0)
        return f

    def _save_to_minio(self, file_name: str, data: io.BytesIO):
        s3.client.put_object(
            config.get_env(config.EnvKeys.MINIO_DATA_EXPORT_BUCKET),
            file_name,
            data,
            length=-1,
            part_size=PART_SIZE,
        )
        return
