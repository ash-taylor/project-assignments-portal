from typing import Annotated, List
from fastapi import APIRouter, Depends

from api.database.models.user import User
from api.dependencies import (
    decode_access_token_dep,
    get_user_service_dep,
    hash_password_dep,
)
from api.schemas.auth import Token, TokenData
from api.schemas.user import UserHashed, UserOut
from api.services.user_service_base import UserServiceBase

router = APIRouter(prefix="/api")


@router.post("/user", tags=["users"], response_model=Token)
async def create_new_user(
    user: Annotated[UserHashed, Depends(hash_password_dep)],
    user_service: Annotated[UserServiceBase, Depends(get_user_service_dep)],
):
    new_user = User(
        user_name=user.user_name,
        hashed_password=user.hashed_password,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        role=user.role,
    )

    return await user_service.create_user(new_user)


@router.get("/users", tags=["users"], response_model=List[UserOut])
async def read_users(
    user_service: Annotated[UserServiceBase, Depends(get_user_service_dep)]
):
    db_users = await user_service.list_users()
    return db_users


@router.get("/users/me", tags=["users"], response_model=UserOut)
async def read_current_user(
    decoded_token: Annotated[TokenData, Depends(decode_access_token_dep)],
    user_service: Annotated[UserServiceBase, Depends(get_user_service_dep)],
):
    return await user_service.get_current_user(decoded_token)
