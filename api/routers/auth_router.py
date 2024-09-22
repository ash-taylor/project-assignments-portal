"""Authentication router module providing entry point for auth API routes."""

import logging
from typing import Annotated
from fastapi import APIRouter, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm

from api.core.config import app_config
from api.dependencies import get_auth_service, validate_user
from api.schemas.auth import TokenData
from api.services.interfaces.auth_service_interface import IAuthService


router = APIRouter(prefix="/api")

logger = logging.getLogger(__name__)


@router.post("/login", status_code=204)
async def login(
    response: Response,
    request: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: Annotated[IAuthService, Depends(get_auth_service)],
):
    """POST /login route

    Validates log in request and sets the cookie with a JWT.

    Args:
        response (Response): FastAPI Response - allows cookie access.
        request (Annotated[OAuth2PasswordRequestForm, Depends): The Form request object.
        auth_service (Annotated[IAuthService, Depends): The application 'Auth' service.
    """

    logger.info("user: %s invoked POST /login", request.username)

    # Validate the request and generate a JWT
    access_token = (await auth_service.login(request)).access_token

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=(int(app_config.access_token_exp_mins) * 60),
        expires=(int(app_config.access_token_exp_mins) * 60),
        secure=True,
        samesite="strict",
    )


@router.post("/logout", status_code=205)
async def logout(
    response: Response,
    token: Annotated[TokenData, Depends(validate_user)],  # User
):
    """POST /logout route

    Removes the token from the cookie so any future requests are invalidated.

    Args:
        response (Response): FastAPI Response - allows cookie management.
        token (Annotated[TokenData, Depends): The JWT from the cookie.
    """

    logger.info("user %s invoked POST /logout", token.username)
    response.delete_cookie("access_token")
