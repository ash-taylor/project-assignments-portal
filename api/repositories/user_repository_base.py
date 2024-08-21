from abc import ABC, abstractmethod
from typing import List, Optional

from api.database.models.user import User


class UserRepositoryBase(ABC):
    @abstractmethod
    async def create_user(self, user: User) -> User:
        pass

    @abstractmethod
    async def list_users(self) -> List[User]:
        pass

    @abstractmethod
    async def find_user(self, params: dict[str, str]) -> Optional[User]:
        pass
