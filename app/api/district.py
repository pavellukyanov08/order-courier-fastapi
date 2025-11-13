from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from starlette import status

from app.models import District
from app.schemas.district import DistrictRead, DistrictCreate
from app.core.database import get_session, AsyncSessionLocal

router = APIRouter()


@router.post('/districts', response_model=DistrictRead, status_code=201)
async def add_district(district: DistrictCreate, db: AsyncSessionLocal = Depends(get_session)):
    try:
        stmt = select(District).where(District.name == district.name)
        result = await db.execute(stmt)
        existing_district = result.scalars().first()

        if existing_district:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Район уже существует")

        new_district = District(
            name=district.name,
        )

        db.add(new_district)
        await db.commit()
        await db.refresh(new_district)

        return new_district

    except Exception as e:
        await db.rollback()
        return f'Ошибка добавления {str(e)}'


@router.get('/districts', response_model=List[DistrictRead])
async def get_districts(district: Optional[str] = None, db: AsyncSessionLocal = Depends(get_session)):
    stmt = select(District)

    if district is not None:
        stmt = stmt.where(District.name == district)

    result = await db.execute(stmt)
    districts = result.scalars().all()

    return [DistrictRead.model_validate(district) for district in districts]