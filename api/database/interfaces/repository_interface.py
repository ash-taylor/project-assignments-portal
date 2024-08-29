from abc import ABC, abstractmethod
from typing import Dict, Generic, List, Optional, TypeVar


T = TypeVar("T")
U = TypeVar("U")


class IRepository(ABC, Generic[T]):
    @abstractmethod
    async def create(self, entity: T) -> T:
        pass

    @abstractmethod
    async def find(
        self,
        params: Dict[str, str],
        and_condition: bool = True,
        load_relation: str | None = None,
    ) -> Optional[List[T]]:
        pass

    @abstractmethod
    async def list_all(self, load_relation: str | None = None) -> List[T]:
        pass

    @abstractmethod
    async def update(
        self,
        parent: T,
        update_attr: str,
        update_val: str | U,
        load_relation: str | None = None,
    ) -> T:
        pass

    @abstractmethod
    async def delete(self, item: T):
        pass
