"""Projects router module providing entry point for all 'project' API routes."""

import logging
from typing import Annotated, List, Union
from fastapi import APIRouter, Depends

from api.dependencies import (
    get_project_service,
    parse_optional_project_id,
    parse_project_id,
    validate_admin,
    validate_user,
)
from api.schemas.auth import TokenData
from api.schemas.project import ProjectCreate, ProjectOut, ProjectUpdate
from api.schemas.relationships import (
    ProjectWithCustomerOut,
    ProjectWithUsersCustomerOut,
)
from api.services.interfaces.project_service_interface import IProjectService


router = APIRouter(prefix="/api")

logger = logging.getLogger(__name__)


@router.post("/project", tags=["projects"], response_model=ProjectOut)
async def create_project(
    token: Annotated[TokenData, Depends(validate_admin)],  # Admin
    project: ProjectCreate,
    project_service: Annotated[IProjectService, Depends(get_project_service)],
):
    """POST /project route

    Validates and creates a new project in the database,

    Args:
        token (Annotated[TokenData, Depends): JWT,
        project (ProjectCreate): The project object - validated by the ProjectCreate model.
        project_service (Annotated[IProjectService, Depends): The application project service.

    Returns:
        Project: The updated project entity - validated against the ProjectOut model.
    """

    logger.info("user: %s invoked POST /project", token.username)
    return await project_service.create_project(project=project)


@router.get(
    "/project",
    tags=["projects"],
    response_model=Union[ProjectWithCustomerOut | ProjectWithUsersCustomerOut],
)
async def get_project(
    token: Annotated[TokenData, Depends(validate_user)],  # User
    project_service: Annotated[IProjectService, Depends(get_project_service)],
    project_id: Annotated[str | None, Depends(parse_optional_project_id)],
    name: str | None = None,
    users: bool = False,
):
    """GET /project route

    Looks for and returns a specified project by id or name.
    Provides option to return the project with related users.

    Args:
        token (Annotated[TokenData, Depends): JWT
        project_service (Annotated[IProjectService, Depends): Project service
        project_id (Annotated[str  |  None, Depends): The project ID to search for.
        name (str | None, optional): The project name to search for. Defaults to None.
        users (bool, optional): Set True if project related 'Users' required in the response.
        Defaults to False.

    Returns:
       Project: The updated project entity
       validated against the ProjectOut | ProjectWithUsersCustomerOut model.
    """

    logger.info("user: %s invoked GET /project", token.username)
    return await project_service.get_project(
        name=name, project_id=project_id, users=users
    )


@router.get(
    "/projects",
    tags=["projects"],
    response_model=List[Union[ProjectWithCustomerOut | ProjectWithUsersCustomerOut]],
)
async def get_all_projects(
    token: Annotated[TokenData, Depends(validate_user)],  # User
    project_service: Annotated[IProjectService, Depends(get_project_service)],
    users: bool = False,
):
    """GET /projects route

    Returns all project entities in the database.

    Args:
        token (Annotated[TokenData, Depends): JWT
        project_service (Annotated[IProjectService, Depends): Project service
        users (bool, optional): Set True if project related 'Users' required in the response.
        Defaults to False.

    Returns:
       List[Project]: A list of all project entities in the database.
    """

    logger.info("user %s invoked GET /projects", token.username)
    return await project_service.list_projects(users=users)


@router.put("/project/{project_id}", tags=["projects"], response_model=ProjectOut)
async def update_project(
    token: Annotated[TokenData, Depends(validate_admin)],  # Admin
    project_service: Annotated[IProjectService, Depends(get_project_service)],
    project_id: Annotated[str, Depends(parse_project_id)],
    project: ProjectUpdate,
):
    """PUT /project/{project_id} route

    Looks for and updates an existing project entity with the requested updates
    (validated against the ProjectUpdate model)

    Args:
        token (Annotated[TokenData, Depends): JWT
        project_service (Annotated[IProjectService, Depends): Project service
        project_id (Annotated[str  |  None, Depends): The project ID to search for.
        project (ProjectUpdate): The project object - validated by the ProjectUpdate model.

    Returns:
        Project: The updated project entity
    """

    logger.info("user: %s invoked PUT /customers/%s", token.username, project_id)
    return await project_service.update_project(project_id=project_id, project=project)


@router.delete("/project/{project_id}", tags=["projects"], status_code=204)
async def delete_project(
    project_id: Annotated[str, Depends(parse_project_id)],
    token: Annotated[TokenData, Depends(validate_admin)],  # Admin
    project_service: Annotated[IProjectService, Depends(get_project_service)],
):
    """DELETE /project/{project_id} route

    Looks for and deletes an existing project entity.

    Args:
        project_id (Annotated[str, Depends): ID of project to delete
        token (Annotated[TokenData, Depends): JWT
        project_service (Annotated[IProjectService, Depends): Project service

    Returns:
        None: A 204 response returned to client if successful.
    """

    logger.info("user: %s invoked DELETE /project/%s", token.username, project_id)
    await project_service.delete_project(project_id=project_id)
