import flask_restx
import uuid

from app.services import perchai as perchai_service


class Individual(flask_restx.Resource):
    def patch(self, individual_id: uuid.UUID):
        return
