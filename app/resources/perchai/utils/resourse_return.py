import uuid


def id_json(id_: uuid.UUID) -> dict:
    return {"id": str(id_)}


def delete_successed(resource_id) -> dict:
    return {"message": f"{str(resource_id)} deleted"}
