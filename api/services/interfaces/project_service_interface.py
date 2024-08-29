from abc import ABC, abstractmethod
from typing import List

from api.database.models import Project
from api.schemas.project import ProjectCreate


class IProjectService(ABC):
    @abstractmethod
    async def create_project(self, project: ProjectCreate):
        pass

    @abstractmethod
    async def get_project(
        self,
        name: str | None = None,
        project_id: str | None = None,
        users: bool = False,
    ) -> Project:
        pass

    @abstractmethod
    async def find_project(
        self,
        load_relation: str | None = None,
        name: str | None = None,
        project_id: str | None = None,
    ) -> Project | None:
        pass

    @abstractmethod
    async def list_projects(self) -> List[Project]:
        pass

    @abstractmethod
    async def delete_project(self, project_id: str) -> None:
        pass
