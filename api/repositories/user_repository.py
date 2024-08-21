from operator import or_
from typing import List
from sqlalchemy import Result, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from api.database.models.user import User
from api.repositories.user_repository_base import UserRepositoryBase


class UserRepository(UserRepositoryBase):
    def __init__(self, session: AsyncSession):
        self.session = session

    def _return_single_result(self, result: Result):
        try:
            return result.scalar_one()
        except NoResultFound:
            return None

    async def list_users(self) -> List[User]:
        statement = select(User)
        result = await self.session.execute(statement)
        return list(result.scalars().all())

    async def create_user(self, user: User) -> User:
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def find_user(self, params: dict[str, str]) -> User | None:
        filters = []
        if "user_id" in params:
            filters.append(User.id == params["user_id"])
        if "username" in params:
            filters.append(User.user_name == params["username"])
        if "user_email" in params:
            filters.append(User.email == params["user_email"])

        if len(filters) > 1:
            statement = select(User).filter(or_(*filters))
        else:
            statement = select(User).where(*filters)

        result = await self.session.execute(statement)
        return self._return_single_result(result)
