from datetime import datetime
from uuid import UUID

from pydantic import Field
from app.models.token import SessionTokenTypeEnum
from app.common.schemas import CamelDTO
from .base import AccessTokenDTO, RefreshTokenDTO, NormalizeDateTimeDTO


class TokenPairDTO(CamelDTO, RefreshTokenDTO, AccessTokenDTO):
    pass


class TokenDataDTO(NormalizeDateTimeDTO):
    token_id: UUID = Field(..., description="Token unique id")
    token_owner: UUID = Field(..., description="Token owner (user_sid)")
    type: SessionTokenTypeEnum = Field(..., description="Token type")
    expired_at: datetime = Field(..., description="Token expired at")
    created_at: datetime = Field(..., description="Token created at")


class GenerateTokenPairDTO(CamelDTO):
    token_owner: UUID = Field(..., description="Token owner (user_sid)")
    fingerprint: str = Field(
        ..., max_length=512, description="Client device id"
    )


class RefreshTokenPairDTO(CamelDTO, RefreshTokenDTO):
    pass


class RevokeAllTokensDTO(CamelDTO):
    token_owner: UUID = Field(..., description="Token owner (user_sid)")


class RevokeTokenPairDTO(GenerateTokenPairDTO):
    pass