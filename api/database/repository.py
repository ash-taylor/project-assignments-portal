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
    Repository for database interaction, utilising SQLAlchemy 2.0 ORM.
    Repository is generic, so can be used in all service layers.

    Args:
        IRepository (Entity): Repository interface defining the CRUD methods required
        for any inheriting repository class.
    """

    def __init__(self, session: AsyncSession, entity: Type[T]) -> None:
        logger.info("Initializing repository")
        self._session = session
        self._entity = entity

    async def create(self, entity: T) -> T:
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

    async def delete(self, item: T):
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
        conditions = [
            getattr(self._entity, key) == value for key, value in params.items()
        ]

        return and_(*conditions) if and_condition else or_(*conditions)

    async def load_awaitables(
        self, load_relations: List[str], results: List[T]
    ) -> None:
        awaitables = []
        for relation in load_relations:
            for result in results:
                if hasattr(result.awaitable_attrs, relation):
                    awaitables.append(getattr(result.awaitable_attrs, relation))
        await gather(*awaitables)
