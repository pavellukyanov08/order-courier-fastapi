from .normalize_datetime import NormalizeDateTimeModel
from uuid import UUID
from typing import Self
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
    location: str | None = Field(None, max_length=256, description="Client location name")
    os: str | None = Field(None, max_length=128, description="Client OS")
    device: str | None = Field(None, max_length=128, description="Client device")
    source: str | None = Field(None,max_length=128, description="Client source (browser name or smth)")
    user_agent: str | None = Field(None, max_length=2048, description="Client user-agent")
    expired_at: datetime = Field(..., description="Token expired at")
    created_at: datetime = Field(..., description="Token created at")

    redis_record_key: str = Field(
        "", exclude=True, description="Record key for redis"
    )

    @staticmethod
    def create_redis_record_key(
        *,
        token_owner: UUID | None = None,
        fingerprint: str | None = None,
        _type: SessionTokenTypeEnum | None = None,
        sid: UUID | None = None,
    ) -> str:
        record_sub = "*" if token_owner is None else token_owner
        record_fingerprint = (
            "*" if fingerprint is None else fingerprint
        )
        record_type = "*" if _type is None else _type
        record_sid = "*" if sid is None else sid
        return (
            f"token:{record_sub}:"
            f"{record_fingerprint}:{record_type}:{record_sid}"
        )

    @model_validator(mode="after")
    def build_redis_record_key(self) -> Self:
        self.redis_record_key = self.construct_redis_record_key(
            token_owner=self.token_owner,
            fingerprint=self.fingerprint,
            _type=self.type,
            sid=self.sid,
        )
        return self