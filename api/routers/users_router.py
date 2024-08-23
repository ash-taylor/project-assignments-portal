from typing import Annotated, List
from fastapi import APIRouter, Depends

from api.database.models import User
from api.dependencies import (
    get_auth_service_dep,
    get_user_service_dep,
    hash_password_dep,
)
from api.schemas.auth import Token
from api.schemas.user import UserHashed, UserOut
from api.services.auth_service import oauth2_scheme
from api.services.interfaces.auth_service_interface import IAuthService
from api.services.interfaces.user_service_interface import IUserService

router = APIRouter(prefix="/api")


@router.post("/user", tags=["users"], response_model=Token)
async def create_db_user(
    user: Annotated[UserHashed, Depends(hash_password_dep)],
    user_service: Annotated[IUserService, Depends(get_user_service_dep)],
):
    db_user = User(
        user_name=user.user_name,
        hashed_password=user.hashed_password,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        role=user.role,
    )

    return await user_service.create_user(db_user)


@router.get("/users", tags=["users"], response_model=List[UserOut])
async def read_users(
    user_service: Annotated[IUserService, Depends(get_user_service_dep)]
):
    db_users = await user_service.list_users()
    return db_users


@router.get("/users/me", tags=["users"], response_model=UserOut)
async def read_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    auth_service: Annotated[IAuthService, Depends(get_auth_service_dep)],
    user_service: Annotated[IUserService, Depends(get_user_service_dep)],
):
    decoded_token = auth_service.decode_jwt(token)
    return await user_service.get_current_user(decoded_token)
