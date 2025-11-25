from datetime import timedelta

from ..district import DistrictRead
from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID

def serialize_timedelta(td: timedelta) -> int:
   return round(td.total_seconds() / 60)


class Courier(BaseModel):
    active_order: dict | None = Field(default=None, description="Active order of courier")
    avg_order_complete_time: timedelta | None = Field(default=None, description="Average order complete time")
    avg_day_orders: float | None = Field(default=None, description="Average day orders")



class CourierBase(Courier):
    pass


class CourierCreate(BaseModel):
    id: int = Field(..., description="ID of courier")
    user_sid: UUID = Field(..., description="User ID")
    districts: list[str]


class CourierUpdate(CourierBase):
    sid: UUID = Field(..., description="SID of user")


class CourierRead(CourierBase):
    id: int = Field(..., description="ID of courier")
    districts: list[DistrictRead] = Field(default=None, description="List of districts")

    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={
            timedelta: serialize_timedelta,
        }
    )
