from typing import Annotated

from fastapi import APIRouter, Body

from app.settings import api_settings
from .deps import UserServiceDep
from app.schemas.user import UserCreate
from app.common.schemas import UserDTO
from app.schemas.user import AuthLoginDTO, AuthLoginResponseDTO

router = APIRouter(
    prefix=api_settings.USERS_PREFIX,
)

@router.post(
    '/register',
    response_model=UserDTO
)
async def register(
    service: UserServiceDep,
    user_data: UserCreate,
) -> UserDTO:
    return await service.create_user(
        data=user_data,
    )


@router.post('/login', response_model=AuthLoginResponseDTO)
async def login(
    service: UserServiceDep,
    data: Annotated[AuthLoginDTO, Body(...)],
) -> AuthLoginResponseDTO:
    return await service.login(user_data=data)