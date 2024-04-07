class PerchMounData:
    def __init__(self, data: list) -> None:
        self.data: list[dict] = self._to_dict(data)

    def to_csv(self):
        column_names = self._get_comma_column_names()
        rows = self._get_comma_rows()
        return f"{column_names}\n{rows}"

    def _to_dict(self, data):
        return [result._asdict() for result in data]

    def _get_comma_column_names(self) -> str:
        return ",".join(self.data[0].keys())

    def _get_comma_rows(self) -> str:
        comma_values = [",".join(row.values()) for row in self.data]
        line_values = "\n".join(comma_values)
        return line_values
