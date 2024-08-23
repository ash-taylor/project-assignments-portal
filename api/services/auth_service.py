from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import InvalidTokenError, decode, encode
from passlib.context import CryptContext


from api.core.config import app_config
from api.database.models import User
from api.database.interfaces.repository_interface import IRepository
from api.schemas.auth import Token, TokenData
from api.services.interfaces.auth_service_interface import IAuthService
from api.utils.exceptions import ExceptionHandler

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


class AuthService(IAuthService):
    def __init__(self, user_repository: IRepository[User]) -> None:
        self._pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self._user_repository = user_repository

    async def login(self, request: OAuth2PasswordRequestForm) -> Token:
        params = {"user_name": request.username}
        response = await self._user_repository.find(params)
        if not response:
            ExceptionHandler.raise_credentials_exception()
        user = response[0]
        if not user:
            ExceptionHandler.raise_credentials_exception()

        if not self.validate_pwd(request.password, user.hashed_password):
            ExceptionHandler.raise_credentials_exception()

        access_token = self.create_jwt(
            data={"sub": user.user_name, "admin": user.admin}
        )

        return Token(access_token=access_token, token_type="Bearer")

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

    def decode_jwt(self, token: Annotated[str, Depends(oauth2_scheme)]) -> TokenData:
        try:
            payload = decode(
                token, app_config.jwt_secret, algorithms=[app_config.jwt_algorithm]
            )
            username = payload.get("sub")
            admin = payload.get("admin")
            if username is None or admin is None:
                ExceptionHandler.raise_credentials_exception()
            decoded_token = TokenData(username=username, admin=admin)
        except InvalidTokenError:
            ExceptionHandler.raise_credentials_exception()
        return decoded_token

    def hash_pwd(self, pt_pwd: str) -> str:
        return self._pwd_context.hash(pt_pwd)

    def validate_pwd(self, pt_pwd: str, hashed_pwd: str):
        return self._pwd_context.verify(pt_pwd, hashed_pwd)
