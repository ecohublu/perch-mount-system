import datetime
import uuid
import summary.filer


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

    def _get_comma_rows(self) -> str:
        comma_values = [
            ",".join([self._value_to_string(value) for value in row.values()])
            for row in self.data
        ]
        line_values = "\n".join(comma_values)
        return line_values

    def _init_file_name(self):
        return f"{self._init_create_date()}_{self._get_8d_uuid()}.csv"

    def _init_create_date(self):
        return datetime.datetime.now().strftime("%Y-%m-%d")

    def _get_8d_uuid(self) -> str:
        return str(uuid.uuid4())[:8]

    def _value_to_string(self, value) -> str:
        return str(value) if value is not None else ""
