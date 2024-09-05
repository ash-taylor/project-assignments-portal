from contextlib import asynccontextmanager
from typing import AsyncIterator


from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    AsyncConnection,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from api.core.config import app_config
from api.utils.exceptions import ExceptionHandler


class Base(AsyncAttrs, DeclarativeBase):
    pass


class DatabaseSessionManager:
    def __init__(self, host: str):
        self.engine = create_async_engine(
            host,
            echo=True if app_config.log_level == "DEBUG" else False,
            poolclass=NullPool,
        )

        self._sessionmaker = async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autocommit=False,
        )

    async def close(self):
        if self.engine is None:
            ExceptionHandler.raise_http_exception(
                500, "Database session not initialised"
            )
        await self.engine.dispose()

    @asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self.engine is None:
            ExceptionHandler.raise_http_exception(
                500, "Database session not initialised"
            )
        async with self.engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            ExceptionHandler.raise_http_exception(
                500, "Database session not initialised"
            )

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
