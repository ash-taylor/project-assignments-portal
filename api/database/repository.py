from typing import Dict, List, Type, TypeVar

from sqlalchemy import and_, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from api.database.interfaces.repository_interface import IRepository


T = TypeVar("T")


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
        self, params: Dict[str, str], and_condition: bool = True
    ) -> List[T] | None:
        filters = self._generate_filters(params, and_condition)
        result = await self._session.execute(select(self._entity).filter(filters))
        return list(result.scalars().all())

    async def list_all(self) -> List[T]:
        result = await self._session.execute(select(self._entity))
        return list(result.scalars().all())

    def _generate_filters(self, params: Dict[str, str], and_condition: bool):
        conditions = [
            getattr(self._entity, key) == value for key, value in params.items()
        ]

        return and_(*conditions) if and_condition else or_(*conditions)
