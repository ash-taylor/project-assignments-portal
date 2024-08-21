from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from api.dependencies import get_auth_service_dep
from api.schemas.auth import Token
from api.services.interfaces.auth_service_interface import IAuthService


router = APIRouter()


@router.post("/login")
async def login(
    request: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: Annotated[IAuthService, Depends(get_auth_service_dep)],
) -> Token:
    return await auth_service.login(request)
