import logging

from app.common.adapters import PostgresStorageAdapter
from app.common.schemas import UserDTO


class CourierService:
    def __init__(
        self,
        *,
        logger: logging.Logger,
        postgres_adapter: PostgresStorageAdapter,
    ) -> None:
        self._logger = logger
        self._postgres_adapter = postgres_adapter

    async def get_couriers(
        self,
        *,
        courier_id: int | None = None
    ) -> list[UserDTO]:
        couriers = await self._postgres_adapter.get_couriers(courier_id=courier_id)
        result = []
        if couriers:
            result = [UserDTO.model_validate(courier) for courier in couriers]

        return result
