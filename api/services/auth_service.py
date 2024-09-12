from datetime import datetime, timedelta, timezone
import logging
from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from jwt import ExpiredSignatureError, InvalidTokenError, PyJWTError, decode, encode
from passlib.context import CryptContext


from api.core.config import app_config
from api.database.models import User
from api.database.interfaces.repository_interface import IRepository
from api.schemas.auth import Token, TokenData
from api.services.interfaces.auth_service_interface import IAuthService
from api.utils.exceptions import (
    DatabaseConnectionError,
    ExceptionHandler,
    InvalidCredentialsError,
    PasswordHashingError,
    RepositoryError,
)


logger = logging.getLogger(__name__)


class AuthService(IAuthService):
    """
    Auth Service Class, inherits from User Service Interface

    Args:
        IAuthService (class): Interface defining methods required for authentication
    """

    def __init__(self, user_repository: IRepository[User]) -> None:
        logger.info("Initializing AuthService")
        self._pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self._user_repository = user_repository

    async def login(self, request: OAuth2PasswordRequestForm) -> Token:
        """Login user function

        Args:
            request (OAuth2PasswordRequestForm): Form request params for OAuth2 login

        Returns:
            Token: JSON Web Token
        """
        try:
            logger.info("Logging in user")
            result = await self._user_repository.find(
                {"user_name": request.username.lower()}
            )
            if not result or result[0] is None:
                raise InvalidCredentialsError("Invalid username or password")

            user = result[0]
            logger.info("User found")

            if not self.validate_pwd(request.password, user.hashed_password):
                raise InvalidCredentialsError("Invalid username or password")
            logger.info("User authenticated")

            access_token = self.create_jwt(
                data={"sub": user.user_name, "admin": user.admin, "id": str(user.id)}
            )
            logger.info("Access token created")

            return Token(access_token=access_token, token_type="Bearer")
        except InvalidCredentialsError as e:
            logger.error("Log in error: %s", e)
            ExceptionHandler.raise_invalid_credentials_exception()
        except DatabaseConnectionError as e:
            logger.error("Database connection error: %s", e)
            ExceptionHandler.raise_internal_server_error()
        except RepositoryError as e:
            logger.error("Repository error: %s", e)
            ExceptionHandler.raise_internal_server_error()
        except Exception as e:
            logger.error("Log in error: %s", e)
            ExceptionHandler.raise_internal_server_error()

    def create_jwt(self, data: dict) -> str:
        try:
            logger.info("Creating JWT")
            exp = datetime.now(timezone.utc) + timedelta(
                minutes=int(app_config.access_token_exp_mins)
            )
            data.update({"exp": exp})
            encoded_jwt = encode(
                data, app_config.jwt_secret, algorithm=app_config.jwt_algorithm
            )
            return encoded_jwt
        except PyJWTError as e:
            logger.error("JWT error: %s", e)
            raise e

    def decode_jwt(
        self, token: Annotated[str, Depends(app_config.oauth2_scheme)]
    ) -> TokenData:
        try:
            logger.info("Decoding JWT")
            payload = decode(
                token, app_config.jwt_secret, algorithms=[app_config.jwt_algorithm]
            )
            username = payload.get("sub")
            admin = payload.get("admin")
            user_id = payload.get("id")
            if username is None or admin is None or id is None:
                raise InvalidCredentialsError("Invalid token payload")
            logger.info("JWT decoded")
            decoded_token = TokenData(username=username, admin=admin, id=user_id)
            return decoded_token
        except ExpiredSignatureError as e:
            logger.error("JWT error: %s", e)
            ExceptionHandler.raise_expired_token_exception()
        except InvalidTokenError as e:
            logger.error("JWT error: %s", e)
            ExceptionHandler.raise_invalid_token_exception()

    def hash_pwd(self, pt_pwd: str) -> str:
        try:
            logger.info("Hashing password")
            return self._pwd_context.hash(pt_pwd)
        except Exception as e:
            logger.error("Hashing error: %s", e)
            raise PasswordHashingError(str(e)) from e

    def validate_pwd(self, pt_pwd: str, hashed_pwd: str):
        try:
            logger.info("Validating password")
            return self._pwd_context.verify(pt_pwd, hashed_pwd)
        except Exception as e:
            logger.error("Hashing verification error: %s", e)
            raise PasswordHashingError(str(e)) from e
