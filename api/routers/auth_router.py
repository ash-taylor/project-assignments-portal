import logging
from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from api.dependencies import get_auth_service
from api.schemas.auth import Token
from api.services.interfaces.auth_service_interface import IAuthService


router = APIRouter()

logger = logging.getLogger(__name__)


@router.post("/login")
async def login(
    request: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: Annotated[IAuthService, Depends(get_auth_service)],
) -> Token:
    logger.info("user: %s invoked POST /login", request.username)
    return await auth_service.login(request=request)
