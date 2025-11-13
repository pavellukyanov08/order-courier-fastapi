from pydantic import BaseModel

from app.schemas.courier import CourierBase


class OrderRead(BaseModel):
    id: int
    name: str
    courier_id : int
    status_id: int
    district_id: int

    model_config = {'from_attributes': True}


class OrderWithCourier(OrderRead):
    courier: CourierBase

    model_config = {'from_attributes': True}


class OrderCreate(BaseModel):
    name: str
    district: str


class OrderCreateResponse(OrderRead):
    courier: CourierBase