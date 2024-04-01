from tool_api.resources import sections

ROUTES = [
    {
        # shift_time
        "route": "shift_time",
        "resources": [sections.TimeShifter],
        "children": [],
    },
]
