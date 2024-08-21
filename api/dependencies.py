from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from jwt import InvalidTokenError, decode
from api.core.config import app_config
from api.database.models.user import User
from api.database.repository import Repository
from api.database.repository_interface import IRepository
from api.database.session import db_session_manager
from api.services.auth_service import AuthService
from api.services.auth_service_base import AuthServiceBase
from api.services.user_service import UserService
from api.schemas.auth import TokenData
from api.schemas.user import UserCreate, UserHashed
from api.utils.auth import auth_handler
from api.utils.exceptions import ExceptionHandler


async def get_db_session_dep():
    async with db_session_manager.session() as session:
        yield session


def get_user_repository_dep(
    session: Annotated[AsyncSession, Depends(get_db_session_dep)]
) -> IRepository:
    return Repository(session, User)


def get_auth_service_dep() -> AuthServiceBase:
    return AuthService()


def get_user_service_dep(
    user_repository: Annotated[Repository, Depends(get_user_repository_dep)],
    auth_service: Annotated[AuthService, Depends(get_auth_service_dep)],
) -> UserService:
    return UserService(user_repository, auth_service)


def hash_password_dep(user: UserCreate) -> UserHashed:
    user_dict = user.model_dump()
    user_dict.update({"hashed_password": auth_handler.hash_password(user.password)})
    hashed = UserHashed(**user_dict)
    return hashed


def decode_access_token_dep(token: Annotated[str, Depends(auth_handler.oauth2_schema)]):
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
