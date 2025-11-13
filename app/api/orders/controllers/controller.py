from fastapi import APIRouter, Body
from typing import Annotated
from app.settings.api import settings
from app.tokens import schemas
from app.api.tokens.controllers.deps import TokenServiceDep
from app.tokens.schemas import GenerateTokenPairDTO


router = APIRouter(
    prefix=settings.ApiSettings.AUTH_TOKENS_PREFIX,
)

@router.post(
    path='/create',
    response_model=schemas.TokenPairDTO
)
async def create_token_pair(
    service: TokenServiceDep,
    data: Annotated[GenerateTokenPairDTO, Body(...)]
) -> schemas.TokenDataDTO:

    return await service.create_token_pair(data)