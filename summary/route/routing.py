from summary.resources import data_export


ROUTES = [
    {
        # data_export
        "route": "data_export",
        "resources": [data_export.ExportData],
        "children": [],
    },
]
