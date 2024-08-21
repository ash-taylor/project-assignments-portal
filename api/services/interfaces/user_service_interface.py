from abc import ABC, abstractmethod
from typing import List, Optional

from api.database.models.user import User
from api.schemas.auth import Token, TokenData


class IUserService(ABC):
    @abstractmethod
    async def create_user(self, user: User) -> Token:
        pass

    @abstractmethod
    async def list_users(self) -> List[User]:
        pass

    @abstractmethod
    async def get_current_user(self, token_data: TokenData) -> User:
        pass

    @abstractmethod
    async def find_user(
        self,
        username: str | None = None,
        user_email: str | None = None,
        user_id: str | None = None,
    ) -> Optional[User]:
        pass
