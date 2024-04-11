from summary.resources import data_export


ROUTES = [
    {
        # data_export
        "route": "data_export",
        "resources": [data_export.ExportData],
        "children": [],
    },
    {
        # preview data_export
        "route": "preview_export",
        "resources": [data_export.PreviewDataExport],
        "children": [],
    },
]
