from typing import List

from api.database.models.user import User
from api.database.repository_interface import IRepository
from api.schemas.auth import Token, TokenData
from api.services.auth_service_base import AuthServiceBase
from api.services.user_service_base import UserServiceBase
from api.utils.exceptions import ExceptionHandler


class UserService(UserServiceBase):
    def __init__(
        self, user_repository: IRepository[User], auth_service: AuthServiceBase
    ) -> None:
        self._user_repository = user_repository
        self._auth_service = auth_service

    async def create_user(self, user: User) -> Token:
        user_exist = await self.find_user(
            username=user.user_name, user_email=user.email
        )

        if user_exist:
            if (
                user_exist.user_name == user.user_name
                and user_exist.email == user.email
            ):
                ExceptionHandler.raise_http_exception(400, "User already exists")
            elif user_exist.user_name == user.user_name:
                ExceptionHandler.raise_http_exception(400, "Username already exists")
            elif user_exist.email == user.email:
                ExceptionHandler.raise_http_exception(400, "Email already exists")

        persisted_user = await self._user_repository.create(user)

        access_token = self._auth_service.create_jwt(
            data={"sub": persisted_user.user_name, "admin": persisted_user.admin}
        )

        return Token(access_token=access_token, token_type="Bearer")

    async def list_users(self) -> List[User]:
        return await self._user_repository.list_all()

    async def get_current_user(self, token_data: TokenData) -> User:
        result = await self._user_repository.find({"user_name": token_data.username})
        if result is None:
            ExceptionHandler.raise_credentials_exception()
        user = result[0]
        if user is None:
            ExceptionHandler.raise_credentials_exception()
        return user

    async def find_user(
        self,
        username: str | None = None,
        user_email: str | None = None,
        user_id: str | None = None,
    ) -> User | None:
        params = {
            key: value
            for key, value in {
                "user_id": user_id,
                "user_name": username,
                "user_email": user_email,
            }.items()
            if value is not None
        }
        result = await self._user_repository.find(params=params, and_condition=False)
        if result is None:
            ExceptionHandler.raise_credentials_exception()
        user = result[0]
        if user is None:
            ExceptionHandler.raise_credentials_exception()
        return user
