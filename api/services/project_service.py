"""The Service layer for all project API routes"""

import logging
from typing import List

from api.database.interfaces.repository_interface import IRepository
from api.database.models import Project
from api.schemas.project import ProjectCreate, ProjectUpdate
from api.services.interfaces.project_service_interface import IProjectService
from api.utils.exceptions import (
    AttributeNotFoundError,
    DatabaseConnectionError,
    ExceptionHandler,
    IntegrityViolationError,
    ProjectAlreadyExistsError,
    ProjectNotFoundError,
    RepositoryError,
)


logger = logging.getLogger(__name__)


class ProjectService(IProjectService):
    """The service for all project routes.
    Contains all business logic

    Args:
        IProjectService: Interface defining required functionalities
    """

    def __init__(self, project_repository: IRepository[Project]) -> None:
        """Initialize the service

        Args:
            project_repository (IRepository[Project]): The repository layer for database interactions
        """

        logger.info("Initializing ProjectService")
        self._project_repository = project_repository

    async def create_project(self, project: ProjectCreate):
        """Functionality for 'Project' entity creation and storage

        Args:
            project (ProjectCreate): Validated Pydantic ProjectCreate model

        Returns:
            Project: The successfully stored and created project
        """

        try:
            logger.info("Creating project")
            if await self.find_project(name=project.name):
                raise ProjectAlreadyExistsError

            db_project = Project(
                name=project.name,
                status=project.status,
                details=project.details,
                customer_id=project.customer_id,
            )
            logger.info("Project created successfully")

            return await self._project_repository.create(db_project)
        except ProjectAlreadyExistsError:
            logger.error("Project already exists")
            ExceptionHandler.raise_already_exists_exception()
        except IntegrityViolationError as e:
            logger.error("Integrity violation: %s", e)
            ExceptionHandler.raise_already_exists_exception()
        except DatabaseConnectionError as e:
            logger.error("Database connection error: %s", e)
            ExceptionHandler.raise_internal_server_error()
        except RepositoryError as e:
            logger.error("Repository error: %s", e)
            ExceptionHandler.raise_internal_server_error()
        except Exception as e:
            logger.error("Error creating project: %s", e)
            ExceptionHandler.raise_internal_server_error()

    async def update_project(self, project_id: str, project: ProjectUpdate) -> Project:
        """Functionality for updating an existing project entity

        Args:
            project_id (str): The ID of project to update
            project (ProjectUpdate): Validated Pydantic ProjectUpdate model

        Returns:
            Project: Updated project
        """

        try:
            logger.info("Updating project")
            db_project = await self.find_project(project_id=project_id)

            if db_project is None:
                raise ProjectNotFoundError

            logger.info("Project found")
            updates = project.model_dump()
            return await self._project_repository.update(db_project, updates=updates)
        except ProjectNotFoundError:
            logger.error("Project not found")
            ExceptionHandler.raise_http_exception(404, "Project not found")
        except IntegrityViolationError as e:
            logger.error("Integrity violation: %s", e)
            ExceptionHandler.raise_already_exists_exception()
        except AttributeNotFoundError as e:
            logger.error("Attribute not found: %s", e)
            ExceptionHandler.raise_http_exception(400, "Customer not found")
        except DatabaseConnectionError as e:
            logger.error("Database connection error: %s", e)
            ExceptionHandler.raise_internal_server_error()
        except RepositoryError as e:
            logger.error("Repository error: %s", e)
            ExceptionHandler.raise_internal_server_error()
        except Exception as e:
            logger.error("Error creating user: %s", e)
            ExceptionHandler.raise_internal_server_error()

    async def get_project(
        self,
        name: str | None = None,
        project_id: str | None = None,
        users: bool = False,
    ) -> Project:
        """Functionality for retrieving a project entity from database

        Args:
            name (str | None, optional): Name of project to find. Defaults to None.
            project_id (str | None, optional): ID of project to find. Defaults to None.
            users (bool, optional): Include project's related users? Defaults to False.

        Returns:
            Project: Retrieved project entity
        """

        try:
            logger.info("Getting project")
            if not name and not project_id:
                raise ValueError("Either name or project_id must be provided")

            project = await self.find_project(
                name=name,
                project_id=project_id,
                load_relations=["users"] if users else None,
            )
            logger.info("Project found")
            if not project:
                raise ProjectNotFoundError
            logger.info("Project found")
            return project
        except ProjectNotFoundError:
            logger.error("Project not found")
            ExceptionHandler.raise_http_exception(404, "Project not found")
        except ValueError as e:
            logger.error("Value error: %s", e)
            ExceptionHandler.raise_http_exception(400, "Bad request")
        except DatabaseConnectionError as e:
            logger.error("Database connection error: %s", e)
            ExceptionHandler.raise_internal_server_error()
        except RepositoryError as e:
            logger.error("Repository error: %s", e)
            ExceptionHandler.raise_internal_server_error()
        except Exception as e:
            logger.error("Error creating user: %s", e)
            ExceptionHandler.raise_internal_server_error()

    async def list_projects(self, users: bool = False) -> List[Project]:
        """Functionality for listing all projects in the database.

        Args:
            users (bool, optional): Include project's related users? Defaults to False.

        Returns:
            List[Project]: A list containing all project entities
        """

        try:
            logger.info("Listing projects")
            projects = await self._project_repository.list_all(
                load_relations=["users"] if users else None
            )
            return projects
        except DatabaseConnectionError as e:
            logger.error("Database connection error: %s", e)
            ExceptionHandler.raise_internal_server_error()
        except RepositoryError as e:
            logger.error("Repository error: %s", e)
            ExceptionHandler.raise_internal_server_error()
        except Exception as e:
            logger.error("Error creating user: %s", e)
            ExceptionHandler.raise_internal_server_error()

    async def find_project(
        self,
        load_relations: List[str] | None = None,
        name: str | None = None,
        project_id: str | None = None,
    ) -> Project | None:
        """Functionality for finding a project in the database.

        Project can be found by either name or ID.

        Args:
            load_relations (List[str] | None, optional): Dict containing any related entities
            to load async. Defaults to None.
            name (str | None, optional): Name of project to find. Defaults to None.
            project_id (str | None, optional): ID of project to find. Defaults to None.

        Returns:
            Project | None: The found project entity or None
        """

        try:
            logger.info("Finding project")
            params = {
                key: value
                for key, value in {
                    "id": project_id,
                    "name": name,
                }.items()
                if value is not None
            }
            if not params:
                logger.error("No parameters provided")
                raise ValueError("No parameters provided")

            result = await self._project_repository.find(
                params=params, and_condition=False, load_relations=load_relations
            )
            logger.info("Project found")
            if not result:
                return None
            return result[0]
        except ValueError as e:
            logger.error("Value error: %s", e)
            ExceptionHandler.raise_http_exception(400, "Bad request")
        except DatabaseConnectionError as e:
            logger.error("Database connection error: %s", e)
            ExceptionHandler.raise_internal_server_error()
        except RepositoryError as e:
            logger.error("Repository error: %s", e)
            ExceptionHandler.raise_internal_server_error()
        except Exception as e:
            logger.error("Error creating user: %s", e)
            ExceptionHandler.raise_internal_server_error()

    async def delete_project(self, project_id: str) -> None:
        """Functionality to find and delete a project entity

        Args:
            project_id (str): The ID of the project to delete

        """

        try:
            logger.info("Deleting project")
            project = await self.find_project(project_id=project_id)
            if project is None:
                raise ProjectNotFoundError
            logger.info("Project found")
            await self._project_repository.delete(project)
        except ProjectNotFoundError as e:
            logger.error("Project not found: %s", e)
            ExceptionHandler.raise_http_exception(404, "Customer not found")
        except DatabaseConnectionError as e:
            logger.error("Database connection error: %s", e)
            ExceptionHandler.raise_internal_server_error()
        except RepositoryError as e:
            logger.error("Repository error: %s", e)
            ExceptionHandler.raise_internal_server_error()
        except Exception as e:
            logger.error("Error creating user: %s", e)
            ExceptionHandler.raise_internal_server_error()
