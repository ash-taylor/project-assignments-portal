"""Module containing custom exception classes and logic"""

from typing import Any, NoReturn
from fastapi import HTTPException


# Repository Layer Exceptions
class RepositoryError(Exception):
    """Base class for repository exceptions."""


class IntegrityViolationError(RepositoryError):
    """Raised when a database integrity constraint is violated."""


class AttributeNotFoundError(RepositoryError):
    """Raised when an attribute is not found in the entity."""


class DatabaseConnectionError(RepositoryError):
    """Raised when there's an error connecting to the database."""


# Service Layer Exceptions
# Auth Service
class AuthServiceError(Exception):
    """Base class for authentication service exceptions."""


class InvalidCredentialsError(AuthServiceError):
    """Raised when the provided credentials are invalid."""


class PasswordHashingError(AuthServiceError):
    """Raised when there's an error hashing or verifying a password."""


# User Service
class UserServiceError(Exception):
    """Base class for user service exceptions."""


class UserNotFoundError(UserServiceError):
    """Raised when a user is not found."""


class UserAlreadyExistsError(UserServiceError):
    """Raised when a user already exists."""


class UsernameAlreadyExistsError(UserServiceError):
    """Raised when a username already exists."""


class EmailAlreadyExistsError(UserServiceError):
    """Raised when an email already exists."""


# Customer Service
class CustomerServiceError(Exception):
    """Base class for customer service exceptions."""


class CustomerNotFoundError(CustomerServiceError):
    """Raised when a customer is not found."""


class CustomerAlreadyExistsError(CustomerServiceError):
    """Raised when a customer already exists."""


# Project Service
class ProjectServiceError(Exception):
    """Base class for project service exceptions."""


class ProjectNotFoundError(ProjectServiceError):
    """Raised when a project is not found."""


class ProjectAlreadyExistsError(ProjectServiceError):
    """Raised when a project already exists."""


class ExceptionHandler:
    """Static class containing frequently used HTTP error responses."""

    @staticmethod
    def raise_http_exception(
        code: int, message: Any, auth_error: bool = False
    ) -> NoReturn:
        headers = {"WWW-Authenticate": "Bearer"} if auth_error else None
        raise HTTPException(status_code=code, detail=message, headers=headers)

    @staticmethod
    def raise_invalid_credentials_exception() -> NoReturn:
        ExceptionHandler.raise_http_exception(
            401, "Invalid username or password", auth_error=True
        )

    @staticmethod
    def raise_credentials_exception() -> NoReturn:
        ExceptionHandler.raise_http_exception(
            401, "Could not validate credentials", auth_error=True
        )

    @staticmethod
    def raise_unauthorized_exception() -> NoReturn:
        ExceptionHandler.raise_http_exception(
            401, "User unauthorized to perform this action", auth_error=True
        )

    @staticmethod
    def raise_invalid_token_exception() -> NoReturn:
        ExceptionHandler.raise_http_exception(401, "Invalid token", auth_error=True)

    @staticmethod
    def raise_expired_token_exception() -> NoReturn:
        ExceptionHandler.raise_http_exception(401, "Token has expired", auth_error=True)

    @staticmethod
    def raise_forbidden_exception() -> NoReturn:
        ExceptionHandler.raise_http_exception(
            403, "User forbidden to perform this action", auth_error=True
        )

    @staticmethod
    def raise_already_exists_exception() -> NoReturn:
        ExceptionHandler.raise_http_exception(409, "Resource already exists")

    @staticmethod
    def raise_internal_server_error() -> NoReturn:
        ExceptionHandler.raise_http_exception(500, "Internal Server Error")
