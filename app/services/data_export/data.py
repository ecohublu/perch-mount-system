from app import model


_DEFAULT_FIELDS = ()

_FIELDS_SETS = {
    "project": (),
    "perch_mount": (),
    "section": (),
    "media": (),
    "individual": (),
    "ml": (),
}


def get_data(additional_field_sets: list[str]):
    fields = _get_fields_by_sets(additional_field_sets)

    return


def _get_fields_by_sets(sets: list[str]) -> list:
    fields = []
    for s in sets:
        if s not in _FIELDS_SETS:
            continue
        fields.extend(_FIELDS_SETS[s])
    return fields
