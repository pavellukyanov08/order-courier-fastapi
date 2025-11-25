from typing import Self
from app.utils.normalize_datetime import NormalizeDateTimeModel
from uuid import UUID
from pydantic import model_validator, Field
from datetime import datetime

from .tokens_enum import SessionTokenTypeEnum


class TokenModel(NormalizeDateTimeModel):
    sid: UUID = Field(..., description="Token sid")
    token_owner: UUID = Field(..., description="Token owner (user_sid")
    type: SessionTokenTypeEnum = Field(..., description="Token type")
    hash: str = Field(..., max_length=1024, description="Token hash")
    fingerprint: str = Field(...,max_length=1024, description="Client device id hash")
    ip: str | None = Field(None, max_length=64, description="Client IP")
    device: str | None = Field(None, max_length=128, description="Client device")
    user_agent: str | None = Field(None, max_length=2048, description="Client user-agent")
    expired_at: datetime = Field(..., description="Token expired at")
    created_at: datetime = Field(..., description="Token created at")

    redis_key: str = Field(
        "", exclude=True, description="Token key for redis"
    )

    @staticmethod
    def build_redis_key(
        *,
        token_owner: UUID | None = None,
        fingerprint: str | None = None,
        _type: SessionTokenTypeEnum | None = None,
        sid: UUID | None = None,
    ) -> str:
        return (
            f"token:{token_owner or '*'}:"
            f"{fingerprint or '*'}:"
            f"{_type or '*'}:"
            f"{sid or '*'}"
        )

    @model_validator(mode="after")
    def create_redis_key(self) -> Self:
        self.redis_key = self.build_redis_key(
            token_owner=self.token_owner,
            fingerprint=self.fingerprint,
            _type=self.type,
            sid=self.sid,
        )
        return self