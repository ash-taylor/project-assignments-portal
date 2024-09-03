from abc import ABC, abstractmethod
from typing import Dict, Generic, List, TypeVar


T = TypeVar("T")


class IRepository(ABC, Generic[T]):
    @abstractmethod
    async def create(self, entity: T) -> T:
        pass

    @abstractmethod
    async def find(
        self,
        params: Dict[str, str],
        and_condition: bool = True,
        load_relations: List[str] | None = None,
    ) -> List[T] | None:
        pass

    @abstractmethod
    async def update(
        self,
        item: T,
        updates: Dict[str, str | None],
        load_relations: List[str] | None = None,
    ) -> T:
        pass

    @abstractmethod
    async def list_all(self, load_relations: List[str] | None = None) -> List[T]:
        pass

    @abstractmethod
    async def delete(self, item: T):
        pass
