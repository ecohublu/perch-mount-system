import flask_restx
import flask_jwt_extended
import uuid

from app.resources.perchai import parsers
import app.services.perchai as perchai_service
import app.resources.perchai.utils as perchai_utils
import app.resources.utils as resource_utils


class Projects(flask_restx.Resource):

    def get(self):
        projects = perchai_service.projects.get_projects()
        return [project.to_dict() for project in projects]

    @flask_jwt_extended.jwt_required()
    @resource_utils.parse_args(parsers.Projects.post)
    def post(self, parsed_args):
        new_project_id = perchai_service.projects.add_project(**parsed_args)
        project = perchai_service.projects.get_project_by_id(new_project_id)
        return project.to_dict()


class Project(flask_restx.Resource):
    def get(self, project_id: uuid.UUID):
        project = perchai_service.projects.get_project_by_id(project_id)
        return project.to_dict()


class Cameras(flask_restx.Resource):
    def get(self):
        cameras = perchai_service.cameras.get_cameras()
        return [camera.to_dict() for camera in cameras]

    @flask_jwt_extended.jwt_required()
    @resource_utils.parse_args(parsers.Cameras.post)
    def post(self, parsed_args):
        new_camera_id = perchai_service.cameras.add_camera(**parsed_args)
        return perchai_utils.id_json(new_camera_id)


class Events(flask_restx.Resource):
    def get(self):
        events = perchai_service.events.get_events()
        return [event.to_dict() for event in events]

    @flask_jwt_extended.jwt_required()
    @resource_utils.parse_args(parsers.Events.post)
    def post(self, parsed_args):
        new_event_id = perchai_service.events.add_event(**parsed_args)
        return perchai_utils.id_json(new_event_id)


class MountTypes(flask_restx.Resource):
    def get(self):
        mount_types = perchai_service.mount_types.get_mount_types()
        return [mount_type.to_dict() for mount_type in mount_types]

    @flask_jwt_extended.jwt_required()
    @resource_utils.parse_args(parsers.MountTypes.post)
    def post(self, parsed_args):
        new_mount_type_id = perchai_service.mount_types.add_mount_types(**parsed_args)
        return perchai_utils.id_json(new_mount_type_id)


class Behaviors(flask_restx.Resource):
    def get(self):
        behaviors = perchai_service.behaviors.get_behaviors()
        return [behavior.to_dict() for behavior in behaviors]

    @flask_jwt_extended.jwt_required()
    @resource_utils.parse_args(parsers.Behaviors.post)
    def post(self, parsed_args):
        new_behavior_id = perchai_service.behaviors.add_behavior(**parsed_args)
        return perchai_utils.id_json(new_behavior_id)
