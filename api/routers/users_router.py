"""Users router module providing entry point for all 'user' API routes."""

import logging
from typing import Annotated, List, Union
from fastapi import APIRouter, Depends, Response

from api.core.config import app_config
from api.dependencies import (
    get_user_service,
    hash_password,
    parse_project_id,
    parse_user_id,
    validate_admin,
    validate_user,
)
from api.schemas.auth import TokenData
from api.schemas.relationships import UserWithProjectOut
from api.schemas.user import UserCreate, UserOut, UserUpdate
from api.services.interfaces.user_service_interface import IUserService

router = APIRouter(prefix="/api")

logger = logging.getLogger(__name__)


@router.post("/user", tags=["users"], status_code=204)
async def create_user(
    response: Response,
    user: Annotated[UserCreate, Depends(hash_password)],
    user_service: Annotated[IUserService, Depends(get_user_service)],
):
    """POST /user route

    Validates and creates a new user in the database.
    Sets a HTTP-only cookie JWT

    Args:
        response (Response): FastAPI Response object to manage cookie
        user (Annotated[UserCreate, Depends): The user object - validated by the UserCreate model.
        user_service (Annotated[IUserService, Depends): The application user service
    """

    logger.info("user: %s invoked POST /user", user.user_name)
    access_token = (await user_service.create_user(user=user)).access_token

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=(int(app_config.access_token_exp_mins) * 60),
        expires=(int(app_config.access_token_exp_mins) * 60),
        secure=True,
        samesite="strict",
    )


@router.patch("/user", tags=["users"], response_model=UserOut)
async def update_self(
    token: Annotated[TokenData, Depends(validate_user)],  # User
    user: UserUpdate,
    user_service: Annotated[IUserService, Depends(get_user_service)],
):
    """PATCH /user route

    Looks for and updates an existing user entity with the requested updates
    (validated against the UserUpdate model)

    Args:
        token (Annotated[TokenData, Depends): JWT
        user_service (Annotated[IUserService, Depends): The application user service
        user (UserUpdate): The user object - validated by the UserUpdate model.

    Returns:
        User: The updated user entity
    """

    logger.info("user: %s invoked PATCH /user", token.username)
    return await user_service.update_user(user_id=str(token.id), user=user)


@router.get(
    "/user/{user_id}",
    tags=["users"],
    response_model=Union[UserOut | UserWithProjectOut],
)
async def get_user(
    user_id: Annotated[str, Depends(parse_user_id)],
    token: Annotated[TokenData, Depends(validate_admin)],  # Admin
    user_service: Annotated[IUserService, Depends(get_user_service)],
    project: bool = False,
):
    """GET /user/{user_id} route

    Looks for and returns a specified user by id.
    Provides option to return the user with related project.

    Args:
        user_id (Annotated[str, Depends): The user ID to search for
        token (Annotated[TokenData, Depends): JWT
        user_service (Annotated[IUserService, Depends): The application user service
        project (bool, optional): Set True if user related 'Project' required in the response.
        Defaults to False.

    Returns:
        User: The updated user entity - validated against the UserOut | UserWithProjectOut model.
    """

    logger.info("user: %s invoked GET /user/%s", token.username, user_id)
    return await user_service.get_user_by_id(user_id=user_id, project=project)


@router.get("/users/me", tags=["users"], response_model=UserWithProjectOut)
async def get_current_user(
    token: Annotated[TokenData, Depends(validate_user)],  # User
    user_service: Annotated[IUserService, Depends(get_user_service)],
):
    """GET /users/me route

    Returns current user to the client based off JWT in the request.

    Args:
        token (Annotated[TokenData, Depends): JWT
        user_service (Annotated[IUserService, Depends): The application user service

    Returns:
        User: The current user - validated against the UserWithProjectOut model
    """

    logger.info("user: %s invoked GET /users/me", token.username)
    return await user_service.get_current_user(token_data=token)


@router.get(
    "/users", tags=["users"], response_model=List[Union[UserOut | UserWithProjectOut]]
)
async def get_all_users(
    token: Annotated[TokenData, Depends(validate_admin)],  # Admin
    user_service: Annotated[IUserService, Depends(get_user_service)],
    projects: bool = False,
):
    """GET /users route

    Returns all user entities in the database.

    Args:
        token (Annotated[TokenData, Depends): JWT
        user_service (Annotated[IUserService, Depends): The application user service
        projects (bool, optional): Set True if user related 'Projects' required in the response.
        Defaults to False.

    Returns:
       List[User]: A list of all user entities in the database.
    """

    logger.info("user: %s invoked GET /users", token.username)
    return await user_service.list_users(projects=projects)


@router.delete("/user/{user_id}", tags=["users"], status_code=204)
async def delete_user(
    user_id: Annotated[str, Depends(parse_user_id)],
    token: Annotated[TokenData, Depends(validate_admin)],  # Admin
    user_service: Annotated[IUserService, Depends(get_user_service)],
):
    """DELETE /user/{user_id} route

    Looks for and deletes an existing user entity.

    Args:
        user_id (Annotated[str, Depends): ID of user to delete
        token (Annotated[TokenData, Depends): JWT
        user_service (Annotated[IUserService, Depends): The application user service

    Returns:
        None: A 204 response returned to client if successful.
    """

    logger.info("user: %s invoked DELETE /user/%s", token.username, user_id)
    await user_service.delete_user(user_id=user_id)


@router.patch(
    "/user/{user_id}/project/{project_id}",
    tags=["users"],
    response_model=UserWithProjectOut,
)
async def add_project_to_user(
    user_id: Annotated[str, Depends(parse_user_id)],
    project_id: Annotated[str, Depends(parse_project_id)],
    token: Annotated[TokenData, Depends(validate_admin)],  # Admin
    user_service: Annotated[IUserService, Depends(get_user_service)],
):
    """PATCH /user/{user_id}/project/{project_id}

    Looks for the requested project and user entities.
    If both exist, adds the project to the user

    Args:
        user_id (Annotated[str, Depends): ID of user to assign project to
        project_id (Annotated[str, Depends): ID of project to add to the user
        token (Annotated[TokenData, Depends): JWT
        user_service (Annotated[IUserService, Depends): The application user service

    Returns:
        User: The user with added project
    """

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
    token: Annotated[TokenData, Depends(validate_admin)],  # Admin
    user_service: Annotated[IUserService, Depends(get_user_service)],
):
    """PATCH /user/{user_id}/unassign_project

    Looks for requested user
    If exists removes the assigned project (if one is assigned)

    Args:
        user_id (Annotated[str, Depends): ID of user to assign project to
        token (Annotated[TokenData, Depends): JWT
        user_service (Annotated[IUserService, Depends): The application user service

    Returns:
        User: The updated user entity
    """

    logger.info(
        "user: %s invoked PATCH /user/%s/unassign_project", token.username, user_id
    )
    return await user_service.update_user_project(user_id=user_id, project_id=None)
