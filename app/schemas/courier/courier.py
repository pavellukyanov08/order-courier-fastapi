from datetime import timedelta
from typing import List
from sqlalchemy.orm import Mapped
from ..district import DistrictRead
from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID

def serialize_timedelta(td: timedelta) -> int:
   return round(td.total_seconds() / 60)


class Courier(BaseModel):
    active_order: Mapped[dict | None] = Field(default=None, description="Active order of courier")
    avg_order_complete_time: Mapped[timedelta | None] = Field(default=None, description="Average order complete time")
    avg_day_orders: Mapped[float | None] = Field(default=None, description="Average day orders")
    user_sid: Mapped[UUID] = Field(..., description="User ID")


class CourierBase(Courier):
    pass


class CourierCreate(CourierBase):
    id: Mapped[int] = Field(..., description="ID of courier")
    districts: List[str]


class CourierUpdate(CourierBase):
    pass


class CourierUpdateBase(CourierBase):
    sid: UUID = Field(..., description="SID of user")


class CourierRead(CourierBase):
    id: Mapped[int] = Field(..., description="ID of courier")

    districts: Mapped[list[DistrictRead]] = Field(default=None, description="List of districts")

    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={
            timedelta: serialize_timedelta,
        }
    )
