from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field
from app.common.enums import UserRoleEnum
from app.schemas.courier import CourierCreate

class User(BaseModel):
    email: EmailStr = Field(..., description="Email address of user")
    username: str = Field(..., description="username of user")


class UserBase(User):
    pass


class UserCreate(UserBase):
    sid: UUID = Field(..., description="SID of user")
    role: UserRoleEnum = Field(..., description="Role of user")
    courier_data: CourierCreate | None = Field(default=None, description="Courier data of user")
    hashed_password: str = Field(..., description="Hashed password of user")
    created_at: datetime = Field(..., description="User created at")
    updated_at: datetime = Field(..., description="User updated at")



class UserUpdate(UserBase):
    sid: UUID = Field(..., description="SID of user")


# class UserRead(UserCreate):
#     pass