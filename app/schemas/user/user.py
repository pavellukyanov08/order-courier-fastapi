from uuid import UUID
from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):
    email: EmailStr = Field(..., description="Email address of user")
    username: str = Field(..., description="username of user")


class UserBase(User):
    pass


class UserCreate(UserBase):
    sid: UUID = Field(..., description="SID of user")
    hashed_password: str = Field(..., description="Password of user")


class UserUpdate(UserBase):
    hashed_password: str = Field(..., description="Password of user")


class UserUpdateBase(UserBase):
    sid: UUID = Field(..., description="SID of user")
    hashed_password: str = Field(..., description="Password of user")


class UserRead(UserBase):
    sid: UUID = Field(..., description="SID of user")