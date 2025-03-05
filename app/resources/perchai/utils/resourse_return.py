import uuid


def id_json(id_: uuid.UUID) -> dict:
    return {"id": str(id_)}
