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
    logger.info("user: %s invoked POST /login", request.username)
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
    token: Annotated[TokenData, Depends(validate_user)],
):
    logger.info("user %s invoked POST /logout", token.username)
    response.delete_cookie("access_token")
