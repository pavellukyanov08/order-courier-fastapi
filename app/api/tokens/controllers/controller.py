from fastapi import APIRouter, Body
from typing import Annotated
from app.settings import api_settings
from app.schemas.tokens import TokenPairDTO, GenerateTokenPairDTO
from app.api.tokens.controllers.deps import TokenServiceDep


router = APIRouter(
    prefix=api_settings.AUTH_TOKENS_PREFIX,
)


@router.post(
    path='/create',
    response_model=TokenPairDTO
)
async def create_token_pair(
    service: TokenServiceDep,
    data: Annotated[GenerateTokenPairDTO, Body(...)]
) -> TokenPairDTO:

    return await service.create_token_pair(data)