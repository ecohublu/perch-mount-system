import flask
import flask_jwt_extended
import http
from google.auth.transport import requests
from google.oauth2 import id_token
import uuid

from app import env
from app.login import user
from app.login import jwt
import app.services.perchai as perchai_service

blueprint = flask.Blueprint("login", __name__)


@blueprint.route("/login", methods=[http.HTTPMethod.POST])
def login_by_google_sso_id_token():
    google_id_token = flask.request.get_json()["id_token"]

    id_info = id_token.verify_oauth2_token(
        google_id_token,
        requests.Request(),
        env.get_env(env.EnvKeys.GOOGLE_OAUTH2_CLIENT_ID),
    )

    signin_user = user.SigningUpGoogleUser(id_info)

    if not signin_user.valid():
        raise

    if signin_user.is_new_user:
        perchai_service.members.add_member_with_sso_info(id_info)

    elif not signin_user.with_sub:
        perchai_service.members.update_member_sso_info(id_info)

    signin_user.refresh_member_info()
    access_token = jwt.create_token_for_signing_user(signin_user)

    return flask.jsonify({"token": access_token})


@blueprint.route("/logout", methods=[http.HTTPMethod.DELETE])
@flask_jwt_extended.jwt_required()
def logout():
    jti = flask_jwt_extended.get_jwt()["jti"]
    jwt.jwt_redis_blocklist.set(jti, "", ex=env.get_jwt_access_token_expires())
    return flask.jsonify(msg="Access token revoked")


@blueprint.route("/me", methods=[http.HTTPMethod.GET])
@flask_jwt_extended.jwt_required()
def me():
    identity = flask_jwt_extended.get_jwt_identity()
    member = perchai_service.members.get_member_by_id(uuid.UUID(identity))
    return flask.jsonify(member.to_dict())
