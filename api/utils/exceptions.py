from typing import NoReturn
from fastapi import HTTPException


class ExceptionHandler:

    @staticmethod
    def raise_http_exception(
        code: int, message: str, auth_error: bool = False
    ) -> NoReturn:
        headers = {"WWW-Authenticate": "Bearer"} if auth_error else None
        raise HTTPException(status_code=code, detail=message, headers=headers)

    @staticmethod
    def raise_credentials_exception() -> NoReturn:
        ExceptionHandler.raise_http_exception(
            401, "Could not validate credentials", auth_error=True
        )
