from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.core.config import app_config
from api.database.interfaces.repository_interface import IRepository
from api.database.models import Customer, User
from api.database.repository import Repository
from api.database.session import db_session_manager
from api.schemas.auth import TokenData
from api.schemas.user import UserCreate
from api.services.auth_service import AuthService
from api.services.customer_service import CustomerService
from api.services.interfaces.auth_service_interface import IAuthService
from api.services.interfaces.customer_service_interface import ICustomerService
from api.services.interfaces.user_service_interface import IUserService
from api.services.user_service import UserService
from api.utils.exceptions import ExceptionHandler


async def get_db_session():
    async with db_session_manager.session() as session:
        yield session


def get_user_repository(
    session: Annotated[AsyncSession, Depends(get_db_session)]
) -> IRepository:
    return Repository(session, User)


def get_customer_repository(
    session: Annotated[AsyncSession, Depends(get_db_session)]
) -> IRepository:
    return Repository(session, Customer)


def get_auth_service(
    user_repository: Annotated[Repository, Depends(get_user_repository)]
) -> IAuthService:
    return AuthService(user_repository)


def get_user_service(
    user_repository: Annotated[Repository, Depends(get_user_repository)],
    auth_service: Annotated[IAuthService, Depends(get_auth_service)],
) -> IUserService:
    return UserService(user_repository, auth_service)


def get_customer_service(
    customer_repository: Annotated[Repository, Depends(get_customer_repository)]
) -> ICustomerService:
    return CustomerService(customer_repository)


def validate_user(
    token: Annotated[str, Depends(app_config.oauth2_scheme)],
    auth_service: Annotated[IAuthService, Depends(get_auth_service)],
) -> TokenData:
    return auth_service.decode_jwt(token)


def validate_admin(token: Annotated[TokenData, Depends(validate_user)]) -> TokenData:
    if token.admin:
        ExceptionHandler.raise_unauthorized_exception()
    return token


def hash_password(
    user: UserCreate,
    auth_service: Annotated[IAuthService, Depends(get_auth_service)],
) -> UserCreate:
    user.password = auth_service.hash_pwd(user.password)
    return user
