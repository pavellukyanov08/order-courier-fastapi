import logging
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.user import UserRead


class PostgresStorageAdapter:
    def __init__(
        self,
        *,
        logger: logging.Logger,
        postgres_read: AsyncSession,
        postgres_write: AsyncSession
    ) -> None:
        self._logger = logger
        self._postgres_read = postgres_read
        self._postgres_write = postgres_write

    async def commit_user(self) -> None:
        try:
            await self._postgres_write.commit()
            self._logger.info("Successfully commited changes")
        except Exception as e:
            self._logger.error("Error while commiting changes: %s", e)
            await self.rollback_user()
            raise

    async def rollback_user(self) -> None:
        try:
            await self._postgres_write.rollback()
            self._logger.info("Successfully rollback changes")
        except Exception as e:
            self._logger.error("Error when cancelling changes: %s", e)
            raise

    @staticmethod
    def _get_user_model(
        *,
        user_model: User
    ) -> UserRead:
        return UserRead(

        )