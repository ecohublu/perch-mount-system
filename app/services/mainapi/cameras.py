from app.services import mainapi
import model
import uuid


def get_cameras() -> list[model.Cameras]:
    with mainapi.session.begin() as session:
        cameras = session.query(model.Cameras).all()
    return cameras


def get_camera_by_id(camera_id: str) -> model.Cameras:
    camera_id = uuid.UUID(camera_id)
    with mainapi.session.begin() as session:
        camera = (
            session.query(model.Cameras).filter(model.Cameras.id == camera_id).first()
        )
    return camera


def add_camera(model_name: str) -> str:
    new_camera = model.Cameras(model_name=model_name)
    with mainapi.session.begin() as session:
        session.add(new_camera)
        session.commit()
    return new_camera.id
