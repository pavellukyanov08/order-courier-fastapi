from xmlrpc.client import DateTime

from pydantic import BaseModel, Field

from app.schemas.user import UserRead


class Order(BaseModel):
    name: str = Field(..., description="Name of order")
    created_time: DateTime = Field(..., description="Time of order creation")
    status: int = Field(..., description="Order status")
    district: int = Field(..., description="Order district")


class OrderBase(Order):
    pass


class OrderCreate(OrderBase):
    courier: UserRead


class OrderUpdate(OrderBase):
    completed_time: DateTime = Field(..., description="Time of order completion")


class OrderUpdateBase(OrderBase):
    id: int = Field(..., description="ID of order")
    completed_time: DateTime = Field(..., description="Time of order completion")


class OrderRead(OrderBase):
    id: int = Field(..., description="ID of order")
    courier: UserRead