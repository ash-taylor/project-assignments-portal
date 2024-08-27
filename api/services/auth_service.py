from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from jwt import ExpiredSignatureError, InvalidTokenError, decode, encode
from passlib.context import CryptContext


from api.core.config import app_config
from api.database.models import User
from api.database.interfaces.repository_interface import IRepository
from api.schemas.auth import Token, TokenData
from api.services.interfaces.auth_service_interface import IAuthService
from api.utils.exceptions import ExceptionHandler


class AuthService(IAuthService):
    def __init__(self, user_repository: IRepository[User]) -> None:
        self._pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self._user_repository = user_repository

    async def login(self, request: OAuth2PasswordRequestForm) -> Token:
        result = await self._user_repository.find({"user_name": request.username})
        if not result or result[0] is None:
            ExceptionHandler.raise_credentials_exception()
        user = result[0]
        if not self.validate_pwd(request.password, user.hashed_password):
            ExceptionHandler.raise_credentials_exception()
        access_token = self.create_jwt(
            data={"sub": user.user_name, "admin": user.admin, "id": str(user.id)}
        )
        return Token(access_token=access_token, token_type="Bearer")

    def create_jwt(self, data: dict) -> str:
        exp = datetime.now(timezone.utc) + timedelta(
            minutes=int(app_config.access_token_exp_mins)
        )
        data.update({"exp": exp})
        encoded_jwt = encode(
            data, app_config.jwt_secret, algorithm=app_config.jwt_algorithm
        )
        return encoded_jwt

    def decode_jwt(
        self, token: Annotated[str, Depends(app_config.oauth2_scheme)]
    ) -> TokenData:
        try:
            payload = decode(
                token, app_config.jwt_secret, algorithms=[app_config.jwt_algorithm]
            )
            username = payload.get("sub")
            admin = payload.get("admin")
            user_id = payload.get("id")
            if username is None or admin is None or id is None:
                ExceptionHandler.raise_credentials_exception()
            decoded_token = TokenData(username=username, admin=admin, id=user_id)
        except ExpiredSignatureError:
            ExceptionHandler.raise_http_exception(403, "Expired token")
        except InvalidTokenError:
            ExceptionHandler.raise_credentials_exception()
        return decoded_token

    def hash_pwd(self, pt_pwd: str) -> str:
        return self._pwd_context.hash(pt_pwd)

    def validate_pwd(self, pt_pwd: str, hashed_pwd: str):
        return self._pwd_context.verify(pt_pwd, hashed_pwd)

    def validate_user(self, token: str) -> None:
        self.decode_jwt(token)

    def is_admin(self, token: TokenData) -> bool:
        return not token.admin
