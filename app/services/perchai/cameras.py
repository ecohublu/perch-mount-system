import uuid

from app.services import perchai
from app import model


def get_cameras() -> list[model.Cameras]:
    with perchai.session.begin() as session:
        cameras = session.query(model.Cameras).all()
    return cameras


def get_camera_by_id(camera_id: str) -> model.Cameras | None:
    camera_id = uuid.UUID(camera_id)
    with perchai.session.begin() as session:
        camera = (
            session.query(model.Cameras).filter(model.Cameras.id == camera_id).first()
        )
    return camera


def add_camera(model_name: str) -> str:
    new_camera = model.Cameras(model_name=model_name)
    with perchai.session.begin() as session:
        session.add(new_camera)
        session.commit()
    return new_camera.id
