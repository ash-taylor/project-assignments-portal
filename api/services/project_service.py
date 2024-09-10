from typing import List

from api.database.interfaces.repository_interface import IRepository
from api.database.models import Project
from api.schemas.project import ProjectCreate, ProjectUpdate
from api.services.interfaces.project_service_interface import IProjectService
from api.utils.exceptions import ExceptionHandler


class ProjectService(IProjectService):
    def __init__(self, project_repository: IRepository[Project]) -> None:
        self._project_repository = project_repository

    async def create_project(self, project: ProjectCreate):
        if await self.find_project(name=project.name):
            ExceptionHandler.raise_http_exception(409, "Project already exists")

        db_project = Project(
            name=project.name,
            status=project.status,
            details=project.details,
            customer_id=project.customer_id,
        )
        return await self._project_repository.create(db_project)

    async def update_project(self, project_id: str, project: ProjectUpdate) -> Project:
        if await self.find_project(name=project.name):
            ExceptionHandler.raise_http_exception(409, "Project name already exists")

        db_project = await self.find_project(project_id=project_id)

        if db_project is None:
            ExceptionHandler.raise_http_exception(404, "Project not found")

        updates = project.model_dump()
        return await self._project_repository.update(db_project, updates=updates)

    async def get_project(
        self,
        name: str | None = None,
        project_id: str | None = None,
        users: bool = False,
    ) -> Project:
        if not name and not project_id:
            ExceptionHandler.raise_http_exception(400, "No project name or ID provided")

        project = await self.find_project(
            name=name,
            project_id=project_id,
            load_relations=["users"] if users else None,
        )

        if not project:
            ExceptionHandler.raise_http_exception(404, "Project not found")
        return project

    async def list_projects(self, users: bool = False) -> List[Project]:
        projects = await self._project_repository.list_all(
            load_relations=["users"] if users else None
        )
        return projects

    async def find_project(
        self,
        load_relations: List[str] | None = None,
        name: str | None = None,
        project_id: str | None = None,
    ) -> Project | None:
        params = {
            key: value
            for key, value in {
                "id": project_id,
                "name": name,
            }.items()
            if value is not None
        }
        result = await self._project_repository.find(
            params=params, and_condition=False, load_relations=load_relations
        )
        if not result:
            return None
        return result[0]

    async def delete_project(self, project_id: str) -> None:
        project = await self.find_project(project_id=project_id)
        if project is None:
            ExceptionHandler.raise_http_exception(404, "Project not found")
        await self._project_repository.delete(project)
