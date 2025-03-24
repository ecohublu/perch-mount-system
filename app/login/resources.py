import flask
from google.auth.transport import requests
from google.oauth2 import id_token

from app import env
from app.login import user
import app.services.perchai as perchai_service

blueprint = flask.Blueprint("login", __name__)


# TODO finish add new user and create jwt token
@blueprint.route("/google_sso_login", methods=["POST"])
def google_login():
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
        pass
    elif not signin_user.with_sub:
        perchai_service.members.update_member_sso_info(id_info)
