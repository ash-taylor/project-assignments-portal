"""Contains all application FastAPI Dependencies for dependency injection"""

import logging
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
from api.utils.exceptions import ExceptionHandler, PasswordHashingError


logger = logging.getLogger(__name__)


async def get_db_session():
    """Utilizes the DB Session Manager to retrieve a DB session.

    Yields:
        AsyncSession: The async database session
    """
    async with db_session_manager.session() as session:
        yield session


def get_user_repository(
    session: Annotated[AsyncSession, Depends(get_db_session)]
) -> IRepository:
    """Factory function that instantiates and returns an instance of a user repository

    Args:
        session (Annotated[AsyncSession, Depends): An async database session

    Returns:
        IRepository: The instantiated user repository
    """

    return Repository(session, User)


def get_customer_repository(
    session: Annotated[AsyncSession, Depends(get_db_session)]
) -> IRepository:
    """Factory function that instantiates and returns an instance of a customer repository

    Args:
        session (Annotated[AsyncSession, Depends): An async database session

    Returns:
        IRepository: The instantiated customer repository
    """

    return Repository(session, Customer)


def get_project_repository(
    session: Annotated[AsyncSession, Depends(get_db_session)]
) -> IRepository:
    """Factory function that instantiates and returns an instance of a project repository

    Args:
        session (Annotated[AsyncSession, Depends): An async database session

    Returns:
        IRepository: The instantiated project repository
    """

    return Repository(session, Project)


def get_auth_service(
    user_repository: Annotated[IRepository, Depends(get_user_repository)]
) -> IAuthService:
    """Factory function that instantiates and returns an instance of a user service

    Args:
        user_repository: (Annotated[IRepository, Depends]): A user repository instance

    Returns:
        IAuthService: The instantiated auth service
    """

    return AuthService(user_repository)


def get_project_service(
    project_repository: Annotated[IRepository, Depends(get_project_repository)]
) -> IProjectService:
    """Factory function that instantiates and returns an instance of a project service

    Args:
        project_repository: (Annotated[IRepository, Depends]): A project repository instance

    Returns:
        IProjectService: The instantiated project service
    """

    return ProjectService(project_repository)


def get_user_service(
    user_repository: Annotated[IRepository, Depends(get_user_repository)],
    auth_service: Annotated[IAuthService, Depends(get_auth_service)],
) -> IUserService:
    """Factory function that instantiates and returns an instance of a user service

    Args:
        user_repository: (Annotated[IRepository, Depends]): A user repository instance
        auth_service: (Annotated[IAuthService, Depends]): An auth service instance

    Returns:
        IUserService: The instantiated user service
    """

    return UserService(user_repository, auth_service)


def get_customer_service(
    customer_repository: Annotated[IRepository, Depends(get_customer_repository)]
) -> ICustomerService:
    """Factory function that instantiates and returns an instance of a customer service

    Args:
        customer_repository: (Annotated[IRepository, Depends]): A customer repository instance

    Returns:
        ICustomerService: The instantiated customer service
    """

    return CustomerService(customer_repository)


def validate_user(
    request: Request,
    auth_service: Annotated[IAuthService, Depends(get_auth_service)],
) -> TokenData:
    """FastAPI Dependency for validating a user at the router layer

    Utilizes the auth service to decode the JWT

    Args:
        request (Request): FastAPI Request containing the cookie
        auth_service (Annotated[IAuthService, Depends): The auth service

    Returns:
        TokenData: Decoded JWT data
    """

    logger.info("Validating user")
    token = request.cookies.get("access_token")
    if token is None:
        ExceptionHandler.raise_credentials_exception()
    return auth_service.decode_jwt(token)


def validate_admin(token: Annotated[TokenData, Depends(validate_user)]) -> TokenData:
    """FastAPI Dependency for authorization of an admin user at the router layer

    Once the user JWT has been validated and decoded, the payload is checked for
    a valid admin: True value.

    Args:
        token (Annotated[TokenData, Depends): Utilizes the validate_user dep to get the JWT

    Returns:
        TokenData: Decoded JWT data
    """

    logger.info("Validating admin")
    if not token.admin:
        logger.error("Forbidden access")
        ExceptionHandler.raise_forbidden_exception()
    logger.info("Admin validated")
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
    """FastAPI Dependency to hash a user password at the router layer
    so no plain-text password is stored in the database.

    Args:
        user_name (Annotated[str, Form): username
        first_name (Annotated[str, Form): first name
        last_name (Annotated[str, Form): last name
        role (Annotated[Roles, Form): role
        email (Annotated[str, Form): email
        password (Annotated[str, Form): plain-text password
        auth_service (Annotated[IAuthService, Depends): auth service

    Returns:
        UserCreate: Pydantic validated UserCreate (containing the hashed password)
    """

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
    except PasswordHashingError as e:
        logger.error("Password hashing error: %s", e)
        ExceptionHandler.raise_internal_server_error()


def parse_uuid(v: UUID4) -> str:
    """Fast API dependency to parse a UUID to a string

    Args:
        v (UUID4): UUID to be parsed

    Returns:
        str: UUID in string format
    """
    return str(v)


def parse_project_id(project_id: UUID4) -> str:
    """Fast API dependency to parse a project ID to a string

    Args:
        project_id (UUID4): project ID to be parsed

    Returns:
        str: project ID in string format
    """

    return parse_uuid(project_id)


def parse_optional_project_id(project_id: UUID4 | None = None) -> str | None:
    """Fast API dependency to parse a project ID to a string when project ID param is optional

    Args:
        project_id (UUID4 | None): project ID to be parsed. Defaults to None.

    Returns:
        str: project ID in string format or None.
    """

    return parse_project_id(project_id) if project_id else None


def parse_customer_id(customer_id: UUID4) -> str:
    """Fast API dependency to parse a customer ID to a string

    Args:
        customer_id (UUID4): customer ID to be parsed

    Returns:
        str: customer ID in string format
    """

    return parse_uuid(customer_id)


def parse_optional_customer_id(customer_id: UUID4 | None = None) -> str | None:
    """Fast API dependency to parse a customer ID to a string when customer ID param is optional

    Args:
        customer_id (UUID4 | None): customer ID to be parsed. Defaults to None.

    Returns:
        str: customer ID in string format or None.
    """

    return parse_customer_id(customer_id) if customer_id else None


def parse_user_id(user_id: UUID4) -> str:
    """Fast API dependency to parse a user ID to a string

    Args:
        user_id (UUID4): user ID to be parsed

    Returns:
        str: user ID in string format
    """

    return parse_uuid(user_id)


def parse_optional_user_id(user_id: UUID4 | None = None) -> str | None:
    """Fast API dependency to parse a user ID to a string when user ID param is optional

    Args:
        user_id (UUID4 | None): user ID to be parsed. Defaults to None.

    Returns:
        str: user ID in string format or None.
    """

    return parse_user_id(user_id) if user_id else None
