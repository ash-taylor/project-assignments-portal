from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from api.database.models.user import User
from api.database.repository import Repository
from api.database.repository_interface import IRepository
from api.database.session import db_session_manager
from api.services.auth_service import AuthService
from api.services.user_service import UserService
from api.schemas.user import UserCreate, UserHashed


async def get_db_session_dep():
    async with db_session_manager.session() as session:
        yield session


def get_user_repository_dep(
    session: Annotated[AsyncSession, Depends(get_db_session_dep)]
) -> IRepository:
    return Repository(session, User)


def get_auth_service_dep(
    user_repository: Annotated[Repository, Depends(get_user_repository_dep)]
) -> AuthService:
    return AuthService(user_repository)


def get_user_service_dep(
    user_repository: Annotated[Repository, Depends(get_user_repository_dep)],
    auth_service: Annotated[AuthService, Depends(get_auth_service_dep)],
) -> UserService:
    return UserService(user_repository, auth_service)


def hash_password_dep(
    user: UserCreate,
    auth_service: Annotated[AuthService, Depends(get_auth_service_dep)],
) -> UserHashed:
    user_dict = user.model_dump()
    user_dict.update({"hashed_password": auth_service.hash_pwd(user.password)})
    hashed = UserHashed(**user_dict)
    return hashed
