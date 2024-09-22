"""The Service layer for all project API routes"""

from typing import List

from api.database.models import User
from api.database.interfaces.repository_interface import IRepository
from api.schemas.auth import Token, TokenData
from api.schemas.user import Roles, UserCreate, UserUpdate
from api.services.interfaces.auth_service_interface import IAuthService
from api.services.interfaces.user_service_interface import IUserService
from api.utils.exceptions import (
    AttributeNotFoundError,
    DatabaseConnectionError,
    EmailAlreadyExistsError,
    ExceptionHandler,
    IntegrityViolationError,
    RepositoryError,
    UserAlreadyExistsError,
    UserNotFoundError,
    UsernameAlreadyExistsError,
)
import logging

logger = logging.getLogger(__name__)


class UserService(IUserService):
    """The service for all user routes.
    Contains all business logic

    Args:
        IUserService: Interface defining required functionalities
    """

    def __init__(
        self,
        user_repository: IRepository[User],
        auth_service: IAuthService,
    ) -> None:
        """Initialize the service

        Args:
            user_repository (IRepository[User]): The repository layer for database interactions
            auth_service (IAuthService): Service containing AuthN / AuthZ functionalities
        """
        logger.info("Initializing UserService")
        self._user_repository = user_repository
        self._auth_service = auth_service

    async def create_user(self, user: UserCreate) -> Token:
        """Functionality for creation and storage of new users.

        Args:
            user (UserCreate): Validated Pydantic UserCreate model

        Returns:
            Token: An encoded JWT
        """

        try:
            logger.info("Creating user")

            existing_user = await self.find_user(
                username=user.user_name, user_email=user.email
            )

            if existing_user:
                if (
                    existing_user.user_name == user.user_name
                    and existing_user.email == user.email
                ):
                    raise UserAlreadyExistsError
                elif existing_user.user_name == user.user_name:
                    raise UsernameAlreadyExistsError
                elif existing_user.email == user.email:
                    raise EmailAlreadyExistsError

            logger.info("User does not exist")
            db_user = User(
                user_name=user.user_name.lower(),
                hashed_password=user.password,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email.lower(),
                role=user.role,
                admin=user.role in Roles.MANAGER,
            )
            persisted_user = await self._user_repository.create(db_user)
            logger.info("User created")

            access_token = self._auth_service.create_jwt(
                data={
                    "sub": persisted_user.user_name,
                    "admin": persisted_user.admin,
                    "id": str(persisted_user.id),
                }
            )

            logger.info("Token created")
            return Token(access_token=access_token, token_type="Bearer")
        except UserAlreadyExistsError as e:
            logger.error("User already exists: %s", e)
            ExceptionHandler.raise_already_exists_exception()
        except UsernameAlreadyExistsError as e:
            logger.error("Username already exists: %s", e)
            ExceptionHandler.raise_http_exception(409, "Username already exists")
        except EmailAlreadyExistsError as e:
            logger.error("Email already exists: %s", e)
            ExceptionHandler.raise_http_exception(409, "Email already exists")
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
            logger.error("Error creating user: %s", e)
            ExceptionHandler.raise_internal_server_error()

    async def update_user(self, user_id: str, user: UserUpdate) -> User:
        """Functionality for updating an existing user entity

        Args:
            user_id (str): The ID of user to update
            user (UserUpdate): Validated Pydantic UserUpdate model

        Returns:
            User: Updated user
        """

        try:
            logger.info("Updating user")
            db_user = await self.find_user(user_id=user_id)

            if db_user is None:
                raise UserNotFoundError

            logger.info("User found")
            updates = user.model_dump()
            return await self._user_repository.update(db_user, updates=updates)
        except UserNotFoundError as e:
            logger.error("User not found: %s", e)
            ExceptionHandler.raise_http_exception(404, "User not found")
        except IntegrityViolationError as e:
            logger.error("Integrity violation: %s", e)
            ExceptionHandler.raise_already_exists_exception()
        except AttributeNotFoundError as e:
            logger.error("Attribute not found: %s", e)
            ExceptionHandler.raise_http_exception(400, "User not found")
        except DatabaseConnectionError as e:
            logger.error("Database connection error: %s", e)
            ExceptionHandler.raise_internal_server_error()
        except RepositoryError as e:
            logger.error("Repository error: %s", e)
            ExceptionHandler.raise_internal_server_error()
        except Exception as e:
            logger.error("Error updating user: %s", e)
            ExceptionHandler.raise_internal_server_error()

    async def get_user_by_id(self, user_id: str, project: bool = False) -> User:
        """Functionality for querying the database for a user, by user ID.

        Args:
            user_id (str | None, optional): ID of user to find. Defaults to None.
            project (bool, optional): Include user's related projects? Defaults to False.

        Returns:
            Project: Retrieved user entity
        """

        try:
            logger.info("Getting user")
            user = await self.find_user(
                user_id=user_id, load_relations=["project"] if project else None
            )

            if user is None:
                raise UserNotFoundError
            logger.info("User found")
            return user
        except UserNotFoundError as e:
            logger.error("User not found: %s", e)
            ExceptionHandler.raise_http_exception(404, "User not found")
        except DatabaseConnectionError as e:
            logger.error("Database connection error: %s", e)
            ExceptionHandler.raise_internal_server_error()
        except RepositoryError as e:
            logger.error("Repository error: %s", e)
            ExceptionHandler.raise_internal_server_error()
        except Exception as e:
            logger.error("Error updating user: %s", e)
            ExceptionHandler.raise_internal_server_error()

    async def list_users(self, projects: bool = False) -> List[User]:
        """Functionality for listing all users in the database.

        Args:
            projects (bool, optional): Include any related projects? Defaults to False.

        Returns:
            List[User]: A list containing all user entities
        """

        try:
            logger.info("Listing users")
            return await self._user_repository.list_all(
                load_relations=["project"] if projects else None
            )
        except DatabaseConnectionError as e:
            logger.error("Database connection error: %s", e)
            ExceptionHandler.raise_internal_server_error()
        except RepositoryError as e:
            logger.error("Repository error: %s", e)
            ExceptionHandler.raise_internal_server_error()
        except Exception as e:
            logger.error("Error updating user: %s", e)
            ExceptionHandler.raise_internal_server_error()

    async def get_current_user(self, token_data: TokenData) -> User:
        logger.info("Getting current user")
        return await self.get_user_by_id(user_id=str(token_data.id), project=True)

    async def find_user(
        self,
        load_relations: List[str] | None = None,
        username: str | None = None,
        user_email: str | None = None,
        user_id: str | None = None,
    ) -> User | None:
        """Functionality for finding a user in the database.

        User can be found by either username, email or ID.

        Args:
            load_relations (List[str] | None, optional): Dict containing any related entities
            to load async. Defaults to None.
            username (str | None, optional): Username of user to find. Defaults to None.
            user_email (str | None, optional): Email address of user to find. Defaults to None.
            user_id (str | None, optional): ID of user to find. Defaults to None.

        Returns:
            Project | None: The found user entity or None
        """

        try:
            logger.info("Finding user")
            params = {
                key: value
                for key, value in {
                    "id": user_id,
                    "user_name": username,
                    "email": user_email,
                }.items()
                if value is not None
            }
            if not params:
                logger.error("No parameters provided")
                raise ValueError("No parameters provided")

            result = await self._user_repository.find(
                params=params, and_condition=False, load_relations=load_relations
            )
            if not result or result[0] is None:
                return None

            logger.info("User found")
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
            logger.error("Error updating user: %s", e)
            ExceptionHandler.raise_internal_server_error()

    async def delete_user(self, user_id: str) -> None:
        """Functionality to find and delete a user entity

        Args:
            user_id (str): The ID of the user to delete

        """

        try:
            logger.info("Deleting user")
            user = await self.find_user(user_id=user_id)

            if user is None:
                raise UserNotFoundError
            logger.info("User found")

            await self._user_repository.delete(user)
            logger.info("User deleted")
        except UserNotFoundError as e:
            logger.error("User not found: %s", e)
            ExceptionHandler.raise_http_exception(404, "User not found")
        except DatabaseConnectionError as e:
            logger.error("Database connection error: %s", e)
            ExceptionHandler.raise_internal_server_error()
        except RepositoryError as e:
            logger.error("Repository error: %s", e)
            ExceptionHandler.raise_internal_server_error()
        except Exception as e:
            logger.error("Error updating user: %s", e)
            ExceptionHandler.raise_internal_server_error()

    async def update_user_project(self, user_id: str, project_id: str | None) -> User:
        """Functionality to update the 'project_id' of a user entity.
        Used to either assign or unassign a project to the user.

        Args:
            user_id (str): The ID of the user
            project_id (str | None): The Project ID to update the user with.
            If None - the user will no longer be assigned a project.

        Returns:
            User: The updated user entity
        """

        try:
            logger.info("Updating user project")
            user = await self.find_user(user_id=user_id)

            if user is None:
                raise UserNotFoundError

            logger.info("User found")
            updated_user = await self._user_repository.update(
                item=user,
                updates={"project_id": project_id},
                load_relations=["project"],
            )

            logger.info("User project updated")
            return updated_user
        except UserNotFoundError as e:
            logger.error("User not found: %s", e)
            ExceptionHandler.raise_http_exception(404, "User not found")
        except IntegrityViolationError as e:
            logger.error("Integrity violation: %s", e)
            ExceptionHandler.raise_already_exists_exception()
        except AttributeNotFoundError as e:
            logger.error("Attribute not found: %s", e)
            ExceptionHandler.raise_http_exception(400, "Not found")
        except DatabaseConnectionError as e:
            logger.error("Database connection error: %s", e)
            ExceptionHandler.raise_internal_server_error()
        except RepositoryError as e:
            logger.error("Repository error: %s", e)
            ExceptionHandler.raise_internal_server_error()
        except Exception as e:
            logger.error("Error updating user: %s", e)
            ExceptionHandler.raise_internal_server_error()
