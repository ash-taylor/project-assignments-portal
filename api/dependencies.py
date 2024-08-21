from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.database.interfaces.repository_interface import IRepository
from api.database.models.user import User
from api.database.repository import Repository
from api.database.session import db_session_manager
from api.schemas.user import UserCreate, UserHashed
from api.services.auth_service import AuthService
from api.services.interfaces.auth_service_interface import IAuthService
from api.services.interfaces.user_service_interface import IUserService
from api.services.user_service import UserService


async def get_db_session_dep():
    async with db_session_manager.session() as session:
        yield session


def get_user_repository_dep(
    session: Annotated[AsyncSession, Depends(get_db_session_dep)]
) -> IRepository:
    return Repository(session, User)


def get_auth_service_dep(
    user_repository: Annotated[Repository, Depends(get_user_repository_dep)]
) -> IAuthService:
    return AuthService(user_repository)


def get_user_service_dep(
    user_repository: Annotated[Repository, Depends(get_user_repository_dep)],
    auth_service: Annotated[IAuthService, Depends(get_auth_service_dep)],
) -> IUserService:
    return UserService(user_repository, auth_service)


def hash_password_dep(
    user: UserCreate,
    auth_service: Annotated[IAuthService, Depends(get_auth_service_dep)],
) -> UserHashed:
    user_dict = user.model_dump()
    user_dict.update({"hashed_password": auth_service.hash_pwd(user.password)})
    hashed = UserHashed(**user_dict)
    return hashed
