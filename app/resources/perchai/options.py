import flask_restx

from app.services import perchai as perchai_service


class Projects(flask_restx.Resource):
    def get(self):
        projects = perchai_service.projects.get_projects()
        return [project.to_dict() for project in projects]


class Cameras(flask_restx.Resource):
    def get(self):
        cameras = perchai_service.cameras.get_cameras()
        return [camera.to_dict() for camera in cameras]


class Events(flask_restx.Resource):
    def get(self):
        events = perchai_service.events.get_events()
        return [event.to_dict() for event in events]


class MountTypes(flask_restx.Resource):
    def get(self):
        mount_types = perchai_service.mount_types.get_mount_types()
        return [mount_type.to_dict() for mount_type in mount_types]


class Behaviors(flask_restx.Resource):
    def get(self):
        behaviors = perchai_service.cameras.get_cameras()
        return [behavior.to_dict() for behavior in behaviors]
