import logging
from typing import cast
from uuid import UUID

from pydantic import EmailStr
from sqlalchemy import ColumnElement, select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.models import User
from app.common.schemas import UserDTO
from app.models.courier import Courier


class PostgresStorageAdapter:
    def __init__(
        self,
        *,
        logger: logging.Logger,
        postgres_session: AsyncSession,

    ) -> None:
        self._logger = logger
        self._postgres_session = postgres_session

    async def commit_user(self) -> None:
        try:
            await self._postgres_session.commit()
            self._logger.info("Changes has been commited")
        except Exception as e:
            self._logger.error("Error while commiting changes: %s", e)
            await self.rollback_user()
            raise

    async def rollback_user(self) -> None:
        try:
            await self._postgres_session.rollback()
            self._logger.info("Changes has been cancelled")
        except Exception as e:
            self._logger.error("Error when cancelling changes: %s", e)
            raise

    @staticmethod
    def _create_user_model(
        *,
        user_alchemy_model: User,
    ) -> UserDTO:
        return UserDTO(
            sid=user_alchemy_model.sid,
            email=cast(EmailStr, user_alchemy_model.email),
            username=user_alchemy_model.username,
            role=user_alchemy_model.role,
            hashed_password=user_alchemy_model.hashed_password,
            created_at=user_alchemy_model.created_at,
            updated_at=user_alchemy_model.created_at,
        )

    async def _get_user_model(
        self,
        *,
        user_result: ColumnElement[bool]
    ) -> UserDTO | None:
        query = select(User).where(user_result)
        stmt = await self._postgres_session.execute(query)
        result = stmt.scalar_one_or_none()

        if result is None:
            return None

        user_dto_model = UserDTO.model_validate(
            obj=result, from_attributes=True
        )
        return user_dto_model


    async def get_user(
        self, *, user_sid: UUID
    ) -> UserDTO | None:
        try:
            user_model = await self._get_user_model(
                user_result=(User.sid == user_sid),
            )
            self._logger.info(
                "Received user user_sid=%s",
                user_sid,
            )
            return user_model
        except Exception as e:
            self._logger.info(
                "Failed receiving user: user_sid=%s error=%s",
                user_sid,
                e,
            )
            raise

    async def get_couriers(
        self, *, courier_id: int | None = None
    ) -> UserDTO | None:
        try:
            courier_model = await self._get_user_model(
                user_result=(Courier.id == courier_id),
            )
            self._logger.info(
                "Received courier courier_id=%s",
                courier_id,
            )
            return courier_model
        except Exception as e:
            self._logger.info(
                "Failed receiving courier: courier_id=%s error=%s",
                courier_id,
                e,
            )
            raise

    async def get_user_by_email(
        self, *, user_email: EmailStr
    ) -> UserDTO | None:
        try:
            user_model = await self._get_user_model(
                user_result=(
                        User.email == user_email
                ),
            )
            self._logger.info(
                "Received user by user_email=%s",
                user_email,
            )
            return user_model
        except Exception as e:
            self._logger.info(
                "Failed to receive user: user_email=%s error=%s",
                user_email,
                e,
            )
            raise

    async def check_user_exists(
        self,
        *,
        user_sid: UUID
    ) -> bool:
        query = select(User.sid).where(User.sid == user_sid)
        stmt = await self._postgres_session.execute(query)
        result = stmt.first()
        if result is None:
            return False
        return True

    async def create_user(
        self,
        *,
        user_model: UserDTO,
    ) -> None:
        courier_data = user_model.courier_data

        try:
            if not await self.check_user_exists(user_sid=user_model.sid):
                user_model = User(
                    sid=user_model.sid,
                    username=user_model.username,
                    email=str(user_model.email),
                    role=user_model.role,
                    hashed_password=user_model.hashed_password,
                    created_at=user_model.created_at,
                    updated_at=user_model.created_at,
                )

                courier = Courier(
                    id=courier_data.id,
                    user_sid=courier_data.user_sid,
                    districts=courier_data.districts,
                    register_at=user_model.courier.register_at,
                )

                self._postgres_session.add(user_model)
                # self._postgres_session.add(courier)

                self._logger.info("User has been created: %s", user_model.sid)
        except Exception as e:
            self._logger.error(
                "Failed creating user: sid=%s error=%s",
                user_model.sid,
                e,
            )
            await self.rollback_user()
            raise

    async def update_user(
        self,
        *,
        user_model: UserDTO,
    ) -> None:
        try:
            query = update(User).where(User.sid == user_model.sid).values(
                email=str(user_model.email),
                username=user_model.username,
                hashed_password=user_model.hashed_password,
            )
            await self._postgres_session.execute(query)
            self._logger.info("User has been updated: %s",
                            user_model.sid
)
        except SQLAlchemyError as e:
            self._logger.info("Error while updating user: %s", e)
            await self.rollback_user()
            raise
