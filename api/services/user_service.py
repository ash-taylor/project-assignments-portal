from typing import List

from api.database.models import User
from api.database.interfaces.repository_interface import IRepository
from api.schemas.auth import Token, TokenData
from api.schemas.user import UserCreate
from api.services.interfaces.auth_service_interface import IAuthService
from api.services.interfaces.user_service_interface import IUserService
from api.utils.exceptions import ExceptionHandler


class UserService(IUserService):
    def __init__(
        self, user_repository: IRepository[User], auth_service: IAuthService
    ) -> None:
        self._user_repository = user_repository
        self._auth_service = auth_service

    async def create_user(self, user: UserCreate) -> Token:
        existing_user = await self.find_user(
            username=user.user_name, user_email=user.email
        )
        if existing_user:
            if (
                existing_user.user_name == user.user_name
                and existing_user.email == user.email
            ):
                ExceptionHandler.raise_http_exception(400, "User already exists")
            elif existing_user.user_name == user.user_name:
                ExceptionHandler.raise_http_exception(400, "Username already exists")
            elif existing_user.email == user.email:
                ExceptionHandler.raise_http_exception(400, "Email already exists")
        db_user = User(
            user_name=user.user_name,
            hashed_password=user.password,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            role=user.role,
        )
        print(db_user)
        persisted_user = await self._user_repository.create(db_user)
        access_token = self._auth_service.create_jwt(
            data={
                "sub": persisted_user.user_name,
                "admin": persisted_user.admin,
                "id": str(persisted_user.id),
            }
        )
        return Token(access_token=access_token, token_type="Bearer")

    async def list_users(self) -> List[User]:
        return await self._user_repository.list_all()

    async def get_current_user(self, token_data: TokenData) -> User:
        user = await self.find_user(user_id=str(token_data.id))
        if not user:
            ExceptionHandler.raise_http_exception(404, "User not found")
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
        if not result or result[0] is None:
            return None
        return result[0]

    async def delete_user(self, user_id) -> None:
        user = await self.find_user(user_id=user_id)
        if user is None:
            ExceptionHandler.raise_http_exception(404, "User not found")
        await self._user_repository.delete(user)
