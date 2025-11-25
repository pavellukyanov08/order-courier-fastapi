from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, field_validator, Field


class AccessTokenDTO(BaseModel):
    access_token: str = Field(
        ..., max_length=4096, description="JWT access token"
    )


class RefreshTokenDTO(BaseModel):
    refresh_token: str = Field(
        ..., max_length=4096, description="JWT refresh token"
    )

class NormalizeDateTimeDTO(BaseModel):
    @field_validator("*", mode="before")
    def normalize_datetime(cls, v: Any) -> Any:
        if isinstance(v, datetime):
            if v.tzinfo is None:
                return v.replace(tzinfo=timezone.utc)
            return v.astimezone(tz=timezone.utc)
        return v


