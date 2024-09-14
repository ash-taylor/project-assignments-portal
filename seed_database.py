import asyncio

from api.core.config import app_config
from api.database.models import User
from api.database.repository import Repository
from api.database.session import DatabaseSessionManager
from api.schemas.user import Roles, UserCreate
from api.services.auth_service import AuthService
from api.utils.exceptions import IntegrityViolationError


async def seed_database():
    db_session_manager = DatabaseSessionManager(
        app_config.database_url,
    )

    async with db_session_manager.session() as session:
        user_repository = Repository(session, User)
        auth_service = AuthService(user_repository)

        try:
            print("Seeding database...\n")

            user = UserCreate(
                user_name=app_config.admin_username,
                first_name=app_config.admin_first_name,
                last_name=app_config.admin_last_name,
                role=Roles.MANAGER,
                email=app_config.admin_email,
                password=app_config.admin_password,
            )

            db_user = User(
                user_name=user.user_name,
                hashed_password=auth_service.hash_pwd(user.password),
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email.lower(),
                role=user.role,
                admin=user.role in Roles.MANAGER,
            )

            await user_repository.create(db_user)

            print("\nDatabase seeded successfully")
        except IntegrityViolationError:
            print("\nDatabase already seeded")


if __name__ == "__main__":
    asyncio.run(seed_database())
