from fastapi import APIRouter, Path
from typing import Annotated

from app.settings.api import api_settings
from app.common.schemas import UserDTO
from app.api.couriers.controllers.deps import CourierServiceDep


router = APIRouter(
    prefix=api_settings.COURIERS_PREFIX
)


@router.get(
    '/get',
    response_model=list[UserDTO],
)
async def get_couriers(
    service: CourierServiceDep,
    courier_id: int | None = None,
) -> list[UserDTO]:
    """
    Get couriers by id
    """
    return await service.get_couriers(courier_id=courier_id)
