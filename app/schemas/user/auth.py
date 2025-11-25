from pydantic import Field

from app.common.schemas import CamelDTO, EmailDTO
from app.schemas.tokens import TokenPairDTO


class AuthLoginDTO(CamelDTO, EmailDTO):
    password: str = Field(
        ...,
        max_length=256,
        description="User password",
    )
    fingerprint: str = Field(..., max_length=512, description="User device id")


class AuthLoginResponseDTO(CamelDTO):
    tokens: TokenPairDTO | None = Field(
        None, description="Auth token pair"
    )