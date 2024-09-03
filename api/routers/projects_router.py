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
    token: Annotated[TokenData, Depends(validate_admin)],
    project: ProjectCreate,
    project_service: Annotated[IProjectService, Depends(get_project_service)],
):
    logger.info("user: %s invoked POST /project", token.username)
    return await project_service.create_project(project=project)


@router.get(
    "/project",
    tags=["projects"],
    response_model=Union[ProjectWithCustomerOut | ProjectWithUsersCustomerOut],
)
async def get_project(
    token: Annotated[TokenData, Depends(validate_user)],
    project_service: Annotated[IProjectService, Depends(get_project_service)],
    project_id: Annotated[str | None, Depends(parse_optional_project_id)],
    name: str | None = None,
    users: bool = False,
):
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
    token: Annotated[TokenData, Depends(validate_admin)],
    project_service: Annotated[IProjectService, Depends(get_project_service)],
    users: bool = False,
):
    logger.info("user %s invoked GET /projects", token.username)
    return await project_service.list_projects(users=users)


@router.put("/project/{project_id}", tags=["projects"], response_model=ProjectOut)
async def update_project(
    token: Annotated[TokenData, Depends(validate_admin)],
    project_service: Annotated[IProjectService, Depends(get_project_service)],
    project_id: Annotated[str, Depends(parse_project_id)],
    project: ProjectUpdate,
):
    print(project)
    logger.info("user: %s invoked PUT /customers/%s", token.username, project_id)
    return await project_service.update_project(project_id=project_id, project=project)


@router.delete("/project/{project_id}", tags=["projects"], status_code=204)
async def delete_project(
    project_id: Annotated[str, Depends(parse_project_id)],
    token: Annotated[TokenData, Depends(validate_admin)],  # Requires admin rights
    project_service: Annotated[IProjectService, Depends(get_project_service)],
):
    logger.info("user: %s invoked DELETE /project/%s", token.username, project_id)
    await project_service.delete_project(project_id=project_id)
