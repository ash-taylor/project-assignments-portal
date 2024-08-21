from abc import ABC, abstractmethod
from typing import Dict, Generic, List, Optional, TypeVar


T = TypeVar("T")


class IRepository(ABC, Generic[T]):
    @abstractmethod
    async def create(self, entity: T) -> T:
        pass

    @abstractmethod
    async def find(
        self, params: Dict[str, str], and_condition: bool = True
    ) -> Optional[List[T]]:
        pass

    @abstractmethod
    async def list_all(self) -> List[T]:
        pass
