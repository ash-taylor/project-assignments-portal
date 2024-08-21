from datetime import datetime, timedelta, timezone

from jwt import encode


from api.core.config import app_config
from api.services.auth_service_base import AuthServiceBase


class AuthService(AuthServiceBase):
    def __init__(self) -> None:
        super().__init__()

    def create_jwt(self, data: dict) -> str:
        to_encode = data.copy()
        exp = datetime.now(timezone.utc) + timedelta(
            float(app_config.access_token_exp_mins)
        )
        to_encode.update({"exp": exp})
        encoded_jwt = encode(
            to_encode, app_config.jwt_secret, algorithm=app_config.jwt_algorithm
        )
        return encoded_jwt
