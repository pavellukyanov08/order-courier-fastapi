from datetime import datetime
from uuid import UUID
from pydantic import Field
from .base import EmailDTO

from app.common.enums import UserRoleEnum
from app.utils.normalize_datetime import NormalizeDateTimeModel
from app.schemas.courier import CourierCreate


class UserDTO(NormalizeDateTimeModel, EmailDTO):
    sid: UUID = Field(..., description="SID of user")
    username: str = Field(..., description="username of user")
    role: UserRoleEnum = Field(..., description="Role of user")
    hashed_password: str = Field(..., description="Password of user")
    courier_data: CourierCreate | None = Field(default=None, description="Courier data")
    created_at: datetime = Field(..., description="User created at")
    updated_at: datetime = Field(..., description="User updated at")
