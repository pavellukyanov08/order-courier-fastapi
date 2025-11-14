from typing import Optional

from pydantic import BaseModel, Field


class District(BaseModel):
    name: str = Field(..., description="Name of district")


class DistrictCreate(District):
    id: int = Field(..., description="ID of district")


class DistrictUpdate(District):
    id: int = Field(..., description="ID of district")


class DistrictRead(District):
    id: int = Field(..., description="ID of district")