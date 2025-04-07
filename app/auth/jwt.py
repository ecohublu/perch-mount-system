import flask_jwt_extended
from app import env
from app.auth import user
import redis

jwt = flask_jwt_extended.JWTManager()


jwt_redis_blocklist = redis.StrictRedis(
    host=env.get_env(env.EnvKeys.CACHE_REDIS_HOST),
    port=env.get_env(env.EnvKeys.CACHE_REDIS_PORT),
    db=0,
    decode_responses=True,
)


def _get_additional_claim_from_user(user: user.SigningUpGoogleUser) -> dict:
    return {
        "is_admin": user.member_info.is_admin,
        "is_super_admin": user.member_info.is_super_admin,
        "blocked": user.member_info.blocked,
        "activated": user.member_info.activated,
    }


def create_token_for_signing_user(user: user.SigningUpGoogleUser) -> str:
    return flask_jwt_extended.create_access_token(
        identity=str(user.member_info.id),
        additional_claims=_get_additional_claim_from_user(user),
    )
