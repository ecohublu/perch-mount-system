from app import env
from app import model
import app.services.perchai as perchai_service


_VALID_ISSUERS = ["accounts.google.com", "https://accounts.google.com"]


class SigningUpGoogleUser:
    def __init__(self, id_token):
        self.iss = id_token["iss"]
        self.oidc_sub = id_token["sub"]
        self.audience = id_token["aud"]
        self.email = id_token["email"]
        self.email_verified = id_token["email_verified"]
        self.picture_url = id_token["picture"]
        self.name = id_token["name"]
        self.given_name = id_token["given_name"]
        self.family_name = id_token["family_name"]
        self.member_info = self._get_member()

    def valid(self) -> bool:
        return self.email_verified and self.is_issuer_google() and self.is_valid_aud()

    def is_issuer_google(self) -> bool:
        return self.iss in _VALID_ISSUERS

    def is_valid_aud(self) -> bool:
        return self.audience == env.get_env(env.EnvKeys.GOOGLE_OAUTH2_CLIENT_ID)

    def _get_member(self) -> model.Members | None:
        member = perchai_service.members.get_member_by_sub_and_gmail(
            self.oidc_sub, self.email
        )
        return member

    @property
    def is_new_user(self) -> bool:
        return self.member_info is not None

    @property
    def with_sub(self) -> bool:
        return self.member_info.oidc_sub is not None
