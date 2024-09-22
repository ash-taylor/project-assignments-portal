from asyncio import gather
import logging
from typing import Dict, List, Type, TypeVar

from sqlalchemy import and_, or_, select
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.ext.asyncio import AsyncSession

from api.database.interfaces.repository_interface import IRepository
from api.database.session import Base
from api.utils.exceptions import (
    AttributeNotFoundError,
    DatabaseConnectionError,
    IntegrityViolationError,
    RepositoryError,
)


T = TypeVar("T", bound=Base)

logger = logging.getLogger(__name__)


class Repository(IRepository[T]):
    """
    Repository for database interaction utilizing SQLAlchemy 2.0 ORM.

    Args:
        IRepository (Entity): Repository interface defining the CRUD methods. T = the database entity for typing.
    """

    def __init__(self, session: AsyncSession, entity: Type[T]) -> None:
        """_summary_

        Args:
            session (AsyncSession): The async SQLAlchemy database session.
            entity (Type[T]): The database entity utilized.
        """
        logger.info("Initializing repository")
        self._session = session
        self._entity = entity

    async def create(self, entity: T) -> T:
        """Create a new entity within the database.

        Args:
            entity (T): The database entity to be created.

        Returns:
            T: The newly created database entity.
        """
        logger.info("Creating entity")
        try:
            self._session.add(entity)
            await self._session.commit()
            await self._session.refresh(entity)
            return entity
        except IntegrityError as e:
            await self._session.rollback()
            logger.error("Integrity Error %s", e)
            raise IntegrityViolationError(str(e)) from e
        except OperationalError as e:
            await self._session.rollback()
            logger.error("Operational Error %s", e)
            raise DatabaseConnectionError(str(e)) from e
        except Exception as e:
            await self._session.rollback()
            logger.error("Repository error %s", e)
            raise RepositoryError(str(e)) from e

    async def find(
        self,
        params: Dict[str, str],
        and_condition: bool = True,
        load_relations: List[str] | None = None,
    ) -> List[T] | None:
        """Attempts to find an entity within the database based on the input params.

        Args:
            params (Dict[str, str]): A dict containing the specific parameters to be queried in the database.
            and_condition (bool, optional): Whether to utilize 'and' when querying for multiple parameters, if 'False' 'OR' is used. Defaults to True.
            load_relations (List[str] | None, optional): Due to the async database engine, an entities relations are not loaded by default.
            Pass in a list of the required relations. Defaults to None.

        Returns:
            List[T] | None: A list of all found entities or None if no entities are found.
        """
        logger.info("Finding entity")
        try:
            if not params:
                return None

            filters = self._generate_filters(params, and_condition)
            results = list(
                (await self._session.execute(select(self._entity).filter(filters)))
                .scalars()
                .all()
            )

            if not load_relations:
                return results

            await self.load_awaitables(load_relations=load_relations, results=results)
            return results
        except OperationalError as e:
            logger.error("Operational Error %s", e)
            raise DatabaseConnectionError(str(e)) from e
        except Exception as e:
            logger.error("Repository error %s", e)
            raise RepositoryError(str(e)) from e

    async def update(
        self,
        item: T,
        updates: Dict[str, str | None],
        load_relations: List[str] | None = None,
    ) -> T:
        """Updates an entity within the database with the input 'updates'.

        Args:
            item (T): The database entity to update,
            updates (Dict[str, str  |  None]): A dict containing the update parameter and update value.
            load_relations (List[str] | None, optional): A list of any entity relations required in the response. Defaults to None.

        Returns:
            T: The updated database entity.
        """
        logger.info("Updating entity")
        try:
            for attr, val in updates.items():
                if not hasattr(item, attr):
                    raise AttributeError(f"Attribute {attr} not in item {item}")
                setattr(item, attr, val)

            await self._session.commit()
            await self._session.refresh(item)

            if not load_relations:
                return item

            await self.load_awaitables(load_relations=load_relations, results=[item])
            return item
        except IntegrityError as e:
            await self._session.rollback()
            logger.error("Integrity Error %s", e)
            raise IntegrityViolationError(str(e)) from e
        except AttributeError as e:
            await self._session.rollback()
            logger.error("Attribute Error %s", e)
            raise AttributeNotFoundError(str(e)) from e
        except OperationalError as e:
            await self._session.rollback()
            logger.error("Operational Error %s", e)
            raise DatabaseConnectionError(str(e)) from e
        except Exception as e:
            await self._session.rollback()
            logger.error("Repository error %s", e)
            raise RepositoryError(str(e)) from e

    async def list_all(self, load_relations: List[str] | None = None) -> List[T]:
        """Lists all specified entities within the database.

        Args:
            load_relations (List[str] | None, optional): A list of any entity relations required in the response. Defaults to None.

        Returns:
            List[T]: A list containing all entities in the database.
        """
        logger.info("Listing all entities")
        try:
            results = list(
                (await self._session.execute(select(self._entity))).scalars().all()
            )

            if not load_relations:
                return results

            await self.load_awaitables(load_relations=load_relations, results=results)
            return results
        except OperationalError as e:
            logger.error("Operational Error %s", e)
            raise DatabaseConnectionError(str(e)) from e
        except Exception as e:
            logger.error("Repository error %s", e)
            raise RepositoryError(str(e)) from e

    async def delete(self, item: T) -> None:
        """Deletes an entity within the database.

        Raises if unsuccessful.

        Args:
            item (T): The database entity to be deleted.

        Returns:
            None
        """
        logger.info("Deleting entity")
        try:
            await self._session.delete(item)
            return await self._session.commit()
        except OperationalError as e:
            await self._session.rollback()
            logger.error("Operational Error %s", e)
            raise DatabaseConnectionError(str(e)) from e
        except IntegrityError as e:
            await self._session.rollback()
            logger.error("Integrity Error %s", e)
            raise IntegrityViolationError(str(e)) from e
        except Exception as e:
            await self._session.rollback()
            logger.error("Repository error %s", e)
            raise RepositoryError(str(e)) from e

    def _generate_filters(self, params: Dict[str, str], and_condition: bool):
        """Iterates through a dict of params to query for and returns the SQLAlchemy 'AND' cor 'OR' query conditions.

        Args:
            params (Dict[str, str]): A dict containing the parameters to be queried for.
            and_condition (bool): Whether to return 'AND' SQLAlchemy queries. If False, 'OR' conditions are returned.

        Returns:
            ColumnElement (bool): SQLAlchemy 2.0 Column Element filters to be input within the SQLAlchemy 2.0 'filter' function.
        """
        conditions = [
            getattr(self._entity, key) == value for key, value in params.items()
        ]

        return and_(*conditions) if and_condition else or_(*conditions)

    async def load_awaitables(
        self, load_relations: List[str], results: List[T]
    ) -> None:
        """Helper function to asynchronously load an entities relations

        Args:
            load_relations (List[str]): A list of the entities required relations.
            results (List[T]): A list of all returned entities in which to load their relations.
        """
        awaitables = []
        # Iterate through each relation to be loaded.
        for relation in load_relations:
            # Iterate through each entity.
            for result in results:
                # If the entity contains the required relation, add the relation to the 'awaitables' list.
                if hasattr(result.awaitable_attrs, relation):
                    awaitables.append(getattr(result.awaitable_attrs, relation))
        # Load all relations in the awaitables list.
        await gather(*awaitables)
