from abc import ABC, abstractmethod
from typing import List, Optional

from api.database.models import User
from api.schemas.auth import Token, TokenData
from api.schemas.user import UserCreate, UserUpdate


class IUserService(ABC):
    @abstractmethod
    async def create_user(self, user: UserCreate) -> Token:
        pass

    @abstractmethod
    async def update_user(self, user_id: str, user: UserUpdate) -> User:
        pass

    @abstractmethod
    async def get_user_by_id(self, user_id: str, project: bool = False) -> User:
        pass

    @abstractmethod
    async def list_users(self, projects: bool = False) -> List[User]:
        pass

    @abstractmethod
    async def get_current_user(self, token_data: TokenData) -> User:
        pass

    @abstractmethod
    async def find_user(
        self,
        load_relations: List[str] | None = None,
        username: str | None = None,
        user_email: str | None = None,
        user_id: str | None = None,
    ) -> Optional[User]:
        pass

    @abstractmethod
    async def delete_user(self, user_id: str) -> None:
        pass

    @abstractmethod
    async def update_user_project(self, user_id: str, project_id: str | None) -> User:
        pass
