import logging
from uuid import uuid4

from app.common.adapters import PostgresStorageAdapter
from app.common.enums import UserRoleEnum
from app.common.schemas import UserDTO
from app.schemas.courier import CourierCreate
from app.schemas.user import UserCreate, AuthLoginDTO, AuthLoginResponseDTO
from app.core import PasswordManager
from app.utils import DateTimeManager


class UserService:
    def __init__(
        self,
        *,
        logger: logging.Logger,
        postgres_adapter: PostgresStorageAdapter

    ) -> None:
        self._logger = logger
        self._postgres_adapter = postgres_adapter

    async def commit_user(self) -> None:
        await self._postgres_adapter.commit_user()

    @staticmethod
    def _get_user_model(
        *,
        user_model: UserDTO | None = None,
        user_data: UserCreate,
    ) -> UserDTO:
        hashed_password = PasswordManager.get_hashed_password(
            password=user_data.hashed_password,
        )
        created_at = DateTimeManager.get_now_utc()
        if user_model:
            base_data = {
                "sid": user_model.sid,
                "email": user_model.email,
                "username": user_model.username,
                "role": user_model.role,
                "hashed_password": user_model.hashed_password,
                "created_at": created_at,
                "updated_at": created_at,
            }
            if user_model.role == UserRoleEnum.Courier:
                courier_data = {
                    "id": user_model.courier_data.id,
                    "user_sid": user_model.courier_data.sid,
                    "districts": user_model.courier_data.districts,
                }
                base_data["courier_data"] = CourierCreate.model_validate(courier_data)

            return UserDTO.model_validate(base_data)

        base_data = {
            "sid": uuid4(),
            "email": user_data.email,
            "username": user_data.username,
            "role": user_data.role,
            "hashed_password": hashed_password,
            "created_at": created_at,
            "updated_at": created_at,
        }
        if user_data.role == UserRoleEnum.Courier:
            courier_data = {
                "id": user_data.courier_data.id,
                "user_sid": user_data.courier_data.user_sid,
                "districts": user_data.courier_data.districts,
            }
            base_data["courier_data"] = CourierCreate.model_validate(courier_data)

        print(f"base_data: {base_data}")
        return UserDTO(**base_data)

    async def login(
        self,
        *,
        user_data: AuthLoginDTO
    ) -> AuthLoginResponseDTO:
        user = await self._postgres_adapter.get_user_by_email(
            user_email=user_data.email,
        )
        if user is None:
            raise ValueError("Такого пользователя не существует")
        if user.hashed_password is None or not PasswordManager.verify_password(
            password=user_data.user_password, hashed_password=user.hashed_password
        ):
            raise ValueError("Неверные пользовательские данные")
        await self._postgres_adapter.commit_user()
        return AuthLoginResponseDTO()


    async def create_user(
        self,
        *,
        data: UserCreate,
    ) -> UserDTO:
         user_by_email = await self._postgres_adapter.get_user_by_email(
             user_email=data.email,
         )
         if user_by_email:
             raise ValueError("Пользователь с такой почтой уже существует")

         user_model = self._get_user_model(
             user_model=user_by_email, user_data=data
         )
         print(f"user_model: {user_model}")
         await self._postgres_adapter.create_user(user_model=user_model)
         await self.commit_user()

         return UserDTO.model_validate(obj=user_model, from_attributes=True)

    async def update_user(
            self,
            *,
            user_model: UserDTO,
    ) -> None:
        return await self._postgres_adapter.update_user(user_model=user_model)


