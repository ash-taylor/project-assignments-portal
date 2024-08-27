import logging
from typing import Annotated, List
from fastapi import APIRouter, Depends

from api.dependencies import (
    get_user_service,
    hash_password,
    validate_admin,
    validate_user,
)
from api.schemas.auth import Token, TokenData
from api.schemas.user import UserCreate, UserOut
from api.services.interfaces.user_service_interface import IUserService

router = APIRouter(prefix="/api")

logger = logging.getLogger(__name__)


@router.post("/user", tags=["users"], response_model=Token)
async def create_user(
    user: Annotated[UserCreate, Depends(hash_password)],
    user_service: Annotated[IUserService, Depends(get_user_service)],
):
    logger.info("user: %s invoked POST /user", user.user_name)
    return await user_service.create_user(user)


@router.get("/users", tags=["users"], response_model=List[UserOut])
async def get_all_users(
    token: Annotated[TokenData, Depends(validate_admin)],  # Requires admin rights
    user_service: Annotated[IUserService, Depends(get_user_service)],
):
    logger.info("user: %s invoked GET /users", token.username)
    return await user_service.list_users()


@router.get("/users/me", tags=["users"], response_model=UserOut)
async def get_current_user(
    token: Annotated[TokenData, Depends(validate_user)],
    user_service: Annotated[IUserService, Depends(get_user_service)],
):
    logger.info("user: %s invoked GET /users/me", token.username)
    return await user_service.get_current_user(token)


@router.delete("/user/{user_id}", tags=["users"], status_code=204)
async def delete_user(
    user_id: str,
    token: Annotated[TokenData, Depends(validate_admin)],  # Requires admin rights
    user_service: Annotated[IUserService, Depends(get_user_service)],
):
    logger.info("user: %s invoked DELETE /user/%s", token.username, user_id)
    await user_service.delete_user(user_id=user_id)
