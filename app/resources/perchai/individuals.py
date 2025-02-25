import flask_restful
import uuid

from app.services import perchai as perchai_service

class Individual(flask_restful.Resource):
    def patch(self, individual_id: uuid.UUID):
        return