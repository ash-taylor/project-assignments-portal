from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from api.database.models.user import User
from api.schemas.user import UserHashed


async def create_user(db: AsyncSession, user: UserHashed):
    user_dict = user.model_dump()
    db_user = User(**user_dict)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def get_user_by_username(db: AsyncSession, username: str):
    result = await db.execute(select(User).filter(User.user_name == username))
    return result.scalar()


async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(User).filter(User.email == email))
    return result.scalar()


async def check_user_exists(db: AsyncSession, username: str, email: str):
    result = await db.execute(
        select(User).where(or_(User.email == email, User.user_name == username))
    )
    return result.scalar()


async def get_all_users(db: AsyncSession):
    result = await db.execute(select(User))
    return result.scalars().all()
