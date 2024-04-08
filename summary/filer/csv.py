import datetime
import uuid
import summary.filer

# TODO
TYPES_MAP = {
    "name": str,
    "perch_mount_name": str,
    "habitat": str,
    "latitude": str,
    "longitude": str,
    "layer": None,
    "camera": 1,
    "medium_datetime": datetime.datetime(2022, 5, 11, 11, 54, 17),
    "prey": False,
    "prey_name": None,
    "ring_number": None,
    "xmax": 0.999772,
    "xmin": 0.654112,
    "ymax": 0.95013,
    "ymin": 0.399243,
    "chinese_common_name_by_ai": "黑翅鳶",
    "scientific_name_by_ai": "Elanus caeruleus",
    "taxon_order_by_ai": 7575,
    "chinese_common_name_by_human": "黑翅鳶",
    "scientific_name_by_human": "Elanus caeruleus",
    "taxon_order_by_human": 7575,
}


class PerchMountCsvData(summary.filer.PerchMounData):

    def __init__(self, data: list) -> None:
        self.file_name = self._init_file_name()
        super().__init__(data)

    def to_csv(self):
        column_names = self._get_comma_column_names()
        rows = self._get_comma_rows()
        return f"{column_names}\n{rows}"

    def _get_comma_column_names(self) -> str:
        return ",".join(self.data[0].keys())

    # TODO fix to csv bug
    def _get_comma_rows(self) -> str:
        comma_values = [",".join((row.values())) for row in self.data]
        line_values = "\n".join(comma_values)
        return line_values

    def _init_file_name(self):
        return f"{self._init_create_date()}_{self._get_8d_uuid()}.csv"

    def _init_create_date(self):
        return datetime.datetime.now().strftime("%Y-%m-%d")

    def _get_8d_uuid(self) -> str:
        return str(uuid.uuid4())[:8]
