from typing import Dict, List, Type, TypeVar

from sqlalchemy import and_, or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from api.database.interfaces.repository_interface import IRepository
from api.database.session import Base
from api.utils.exceptions import ExceptionHandler


T = TypeVar("T", bound=Base)
U = TypeVar("U")


class Repository(IRepository[T]):

    def __init__(self, session: AsyncSession, entity: Type[T]) -> None:
        self._session = session
        self._entity = entity

    async def create(self, entity: T) -> T:
        self._session.add(entity)
        await self._session.commit()
        await self._session.refresh(entity)
        return entity

    async def find(
        self,
        params: Dict[str, str],
        and_condition: bool = True,
        load_relation: str | None = None,
    ) -> List[T] | None:
        if not params:
            return None
        filters = self._generate_filters(params, and_condition)
        results = list(
            (await self._session.execute(select(self._entity).filter(filters)))
            .scalars()
            .all()
        )

        if load_relation:
            for result in results:
                if hasattr(result.awaitable_attrs, load_relation):
                    await getattr(result.awaitable_attrs, load_relation)

        return results

    async def update(
        self,
        parent: T,
        update_attr: str,
        update_val: str | U,
        load_relation: str | None = None,
    ) -> T:
        try:
            if not hasattr(parent, update_attr):
                raise AttributeError(
                    f"{self._entity.__name__} does not have a relationship attribute '{update_attr}'."
                )
            update = getattr(parent, update_attr)
            if isinstance(update, list):
                update.append(update_val)
            else:
                setattr(parent, update_attr, update_val)
            await self._session.commit()
            await self._session.refresh(parent)

            if load_relation and hasattr(parent.awaitable_attrs, load_relation):
                await getattr(parent.awaitable_attrs, load_relation)

            return parent
        except IntegrityError:
            ExceptionHandler.raise_http_exception(401, "Bad request")

    async def list_all(self, load_relation: str | None = None) -> List[T]:
        results = list(
            (await self._session.execute(select(self._entity))).scalars().all()
        )

        if load_relation:
            for result in results:
                if hasattr(result.awaitable_attrs, load_relation):
                    await getattr(result.awaitable_attrs, load_relation)

        return results

    def _generate_filters(self, params: Dict[str, str], and_condition: bool):
        conditions = [
            getattr(self._entity, key) == value for key, value in params.items()
        ]

        return and_(*conditions) if and_condition else or_(*conditions)

    async def delete(self, item: T):
        await self._session.delete(item)
        return await self._session.commit()
