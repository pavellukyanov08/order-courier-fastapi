from typing import Annotated
from fastapi import Depends

from app.common.deps import CommonPostgresDep
from app.services.couriers import CourierService
from app.utils import LoggerDep


def _get_courier_service(
        logger: LoggerDep,
        postgres_adapter: CommonPostgresDep
) -> CourierService:
    return CourierService(
        logger=logger,
        postgres_adapter=postgres_adapter
    )


CourierServiceDep = Annotated[CourierService, Depends(_get_courier_service)]
