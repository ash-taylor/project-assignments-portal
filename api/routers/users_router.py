import logging
from typing import Annotated, List, Union
from fastapi import APIRouter, Depends

from api.dependencies import (
    get_user_service,
    hash_password,
    parse_project_id,
    parse_user_id,
    validate_admin,
    validate_user,
)
from api.schemas.auth import Token, TokenData
from api.schemas.relationships import UserWithProjectOut
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
    return await user_service.create_user(user=user)


@router.get(
    "/user/{user_id}",
    tags=["users"],
    response_model=Union[UserOut | UserWithProjectOut],
)
async def get_user(
    user_id: Annotated[str, Depends(parse_user_id)],
    token: Annotated[TokenData, Depends(validate_admin)],
    user_service: Annotated[IUserService, Depends(get_user_service)],
    project: bool = False,
):
    logger.info("user: %s invoked GET /user/%s", token.username, user_id)
    return await user_service.get_user_by_id(user_id=user_id, project=project)


@router.get("/users/me", tags=["users"], response_model=UserWithProjectOut)
async def get_current_user(
    token: Annotated[TokenData, Depends(validate_user)],
    user_service: Annotated[IUserService, Depends(get_user_service)],
):
    logger.info("user: %s invoked GET /users/me", token.username)
    return await user_service.get_current_user(token_data=token)


@router.get(
    "/users", tags=["users"], response_model=List[Union[UserOut | UserWithProjectOut]]
)
async def get_all_users(
    token: Annotated[TokenData, Depends(validate_admin)],  # Requires admin rights
    user_service: Annotated[IUserService, Depends(get_user_service)],
    projects: bool = False,
):
    logger.info("user: %s invoked GET /users", token.username)
    return await user_service.list_users(projects=projects)


@router.delete("/user/{user_id}", tags=["users"], status_code=204)
async def delete_user(
    user_id: Annotated[str, Depends(parse_user_id)],
    token: Annotated[TokenData, Depends(validate_admin)],  # Requires admin rights
    user_service: Annotated[IUserService, Depends(get_user_service)],
):
    logger.info("user: %s invoked DELETE /user/%s", token.username, user_id)
    await user_service.delete_user(user_id=user_id)


@router.patch(
    "/user/{user_id}/project/{project_id}/",
    tags=["users"],
    response_model=UserWithProjectOut,
)
async def add_project_to_user(
    user_id: Annotated[str, Depends(parse_user_id)],
    project_id: Annotated[str, Depends(parse_project_id)],
    token: Annotated[TokenData, Depends(validate_admin)],
    user_service: Annotated[IUserService, Depends(get_user_service)],
):
    logger.info(
        "user: %s invoked PATCH /user/%s/project/%s",
        token.username,
        user_id,
        project_id,
    )
    return await user_service.update_user_project(
        user_id=user_id, project_id=project_id
    )


@router.patch(
    "/user/{user_id}/unassign_project", tags=["users"], response_model=UserOut
)
async def remove_project_from_user(
    user_id: Annotated[str, Depends(parse_user_id)],
    token: Annotated[TokenData, Depends(validate_admin)],
    user_service: Annotated[IUserService, Depends(get_user_service)],
):
    logger.info(
        "user: %s invoked PATCH /user/%s/unassign_project", token.username, user_id
    )
    return await user_service.update_user_project(user_id=user_id, project_id=None)
