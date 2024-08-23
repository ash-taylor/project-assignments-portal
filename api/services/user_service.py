from typing import List

from api.database.models import User
from api.database.interfaces.repository_interface import IRepository
from api.schemas.auth import Token, TokenData
from api.services.interfaces.auth_service_interface import IAuthService
from api.services.interfaces.user_service_interface import IUserService
from api.utils.exceptions import ExceptionHandler


class UserService(IUserService):
    def __init__(
        self, user_repository: IRepository[User], auth_service: IAuthService
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
                "id": user_id,
                "user_name": username,
                "email": user_email,
            }.items()
            if value is not None
        }
        result = await self._user_repository.find(params=params, and_condition=False)

        if not result:
            return None

        user = result[0]

        if user is None:
            ExceptionHandler.raise_http_exception(404, "User not found")

        return user

    async def delete_user(self, user_id) -> None:
        user = await self.find_user(user_id=user_id)

        if user is None:
            ExceptionHandler.raise_http_exception(404, "User not found")
        await self._user_repository.delete(user)
