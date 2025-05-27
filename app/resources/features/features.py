import flask_restx

import app.resources.features.parsers as parsers
import app.resources.utils as resource_utils
import app.services.features.features as features_service


class Features(flask_restx.Resource):
    @resource_utils.parse_args(parsers.Features.get)
    def get(self, parsed_args):
        print(parsed_args)
        count, media = features_service.get_featrues_media(**parsed_args)
        return {
            "total": count,
            "media": [medium.to_dict() for medium in media],
        }
