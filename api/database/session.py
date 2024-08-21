from contextlib import asynccontextmanager
from typing import AsyncIterator

from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.ext.declarative import declarative_base

from api.core.config import app_config

Base = declarative_base()


class DatabaseSessionManager:
    def __init__(self, host: str):
        self.engine = create_async_engine(host)
        self._sessionmaker = async_sessionmaker(autocommit=False, bind=self.engine)

    async def close(self):
        if self.engine is None:
            raise Exception("Database session not initialised")
        await self.engine.dispose()

    @asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self.engine is None:
            raise Exception("Database session not initialised")
        async with self.engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise Exception("Database session not initialised")

        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


db_session_manager = DatabaseSessionManager(
    app_config.database_url,
)
