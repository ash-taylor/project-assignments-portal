from contextlib import asynccontextmanager
import logging
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


logger = logging.getLogger(__name__)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class DatabaseSessionManager:
    def __init__(self, host: str):
        logger.info("Initialising database session manager")
        self.engine = create_async_engine(
            host,
            echo=True if app_config.db_echo == "TRUE" else False,
            poolclass=NullPool,
        )

        self._sessionmaker = async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autocommit=False,
        )

    async def close(self):
        logger.info("Closing database session manager")
        if self.engine is None:
            logger.warning("Database session manager is already closed")
            ExceptionHandler.raise_http_exception(
                500, "Database session not initialised"
            )
        logger.info("Disposing database engine")
        await self.engine.dispose()

    @asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        logger.info("Connecting to database")
        if self.engine is None:
            logger.warning("Database session manager is not initialised")
            ExceptionHandler.raise_http_exception(
                500, "Database session not initialised"
            )
        async with self.engine.begin() as connection:
            logger.info("Database connection established")
            try:
                logger.info("Yielding database connection")
                yield connection
            except Exception:
                logger.error("Database connection error", exc_info=True)
                await connection.rollback()
                raise

    @asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        logger.info("Opening database session")
        if self._sessionmaker is None:
            logger.warning("Database session manager is not initialised")
            ExceptionHandler.raise_http_exception(
                500, "Database session not initialised"
            )

        session = self._sessionmaker()
        logger.info("Database session opened")
        try:
            logger.info("Yielding database session")
            yield session
        except Exception:
            logger.error("Database session error", exc_info=True)
            await session.rollback()
            raise
        finally:
            logger.info("Closing database session")
            await session.close()


db_session_manager = DatabaseSessionManager(
    app_config.database_url,
)
