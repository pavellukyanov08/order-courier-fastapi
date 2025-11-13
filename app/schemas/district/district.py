from typing import Optional

from pydantic import BaseModel


class DistrictRead(BaseModel):
    id: int
    name: Optional[str] = None

    model_config = {
        'from_attributes': True
    }


class DistrictCreate(BaseModel):
    name: str