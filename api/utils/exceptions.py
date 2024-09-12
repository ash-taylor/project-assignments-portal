from typing import Any, NoReturn
from fastapi import HTTPException


class ExceptionHandler:

    @staticmethod
    def raise_http_exception(
        code: int, message: Any, auth_error: bool = False
    ) -> NoReturn:
        headers = {"WWW-Authenticate": "Bearer"} if auth_error else None
        raise HTTPException(status_code=code, detail=message, headers=headers)

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
