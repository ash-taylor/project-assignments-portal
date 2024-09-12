from typing import Annotated

from fastapi import Depends, Form, Request
from pydantic import UUID4, ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from api.database.interfaces.repository_interface import IRepository
from api.database.models import Customer, Project, User
from api.database.repository import Repository
from api.database.session import db_session_manager
from api.schemas.auth import TokenData
from api.schemas.user import Roles, UserCreate
from api.services.auth_service import AuthService
from api.services.customer_service import CustomerService
from api.services.interfaces.auth_service_interface import IAuthService
from api.services.interfaces.customer_service_interface import ICustomerService
from api.services.interfaces.project_service_interface import IProjectService
from api.services.interfaces.user_service_interface import IUserService
from api.services.project_service import ProjectService
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


def get_project_repository(
    session: Annotated[AsyncSession, Depends(get_db_session)]
) -> IRepository:
    return Repository(session, Project)


def get_auth_service(
    user_repository: Annotated[Repository, Depends(get_user_repository)]
) -> IAuthService:
    return AuthService(user_repository)


def get_project_service(
    project_repository: Annotated[Repository, Depends(get_project_repository)]
) -> IProjectService:
    return ProjectService(project_repository)


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
    request: Request,
    auth_service: Annotated[IAuthService, Depends(get_auth_service)],
) -> TokenData:
    token = request.cookies.get("access_token")
    if token is None:
        ExceptionHandler.raise_credentials_exception()
    return auth_service.decode_jwt(token)


def validate_admin(token: Annotated[TokenData, Depends(validate_user)]) -> TokenData:
    if not token.admin:
        ExceptionHandler.raise_forbidden_exception()
    return token


def hash_password(
    user_name: Annotated[str, Form()],
    first_name: Annotated[str, Form()],
    last_name: Annotated[str, Form()],
    role: Annotated[Roles, Form()],
    email: Annotated[str, Form()],
    password: Annotated[str, Form()],
    auth_service: Annotated[IAuthService, Depends(get_auth_service)],
) -> UserCreate:
    try:
        user = UserCreate(
            user_name=user_name,
            first_name=first_name,
            last_name=last_name,
            role=role,
            email=email,
            password=password,
        )
        user.password = auth_service.hash_pwd(user.password)
        return user
    except ValidationError as e:
        errors = e.errors()
        ExceptionHandler.raise_http_exception(400, errors[0])


def parse_uuid(v: UUID4) -> str:
    return str(v)


def parse_project_id(project_id: UUID4) -> str:
    return parse_uuid(project_id)


def parse_optional_project_id(project_id: UUID4 | None = None) -> str | None:
    return parse_project_id(project_id) if project_id else None


def parse_customer_id(customer_id: UUID4) -> str:
    return parse_uuid(customer_id)


def parse_optional_customer_id(customer_id: UUID4 | None = None) -> str | None:
    return parse_customer_id(customer_id) if customer_id else None


def parse_user_id(user_id: UUID4) -> str:
    return parse_uuid(user_id)


def parse_optional_user_id(user_id: UUID4 | None = None) -> str | None:
    return parse_user_id(user_id) if user_id else None
