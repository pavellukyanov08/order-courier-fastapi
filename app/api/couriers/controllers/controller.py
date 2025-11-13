from fastapi import APIRouter, Depends, HTTPException, Body, Path, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from sqlalchemy.orm import selectinload

from app.settings.api import ApiSettings
from app import models, schemas
from app.core import database
from app.api.deps import


router = APIRouter(
    prefix=ApiSettings.COURIERS_PREFIX
)


@router.get(
    '/couriers',
    response_model=list[schemas.CourierRead] | schemas.CourierRead,
)
async def get_couriers(
    idx: Annotated[int | None, Path(..., alias="id")],
    db: Annotated[AsyncSession, Depends(database.get_db)],
    service: TokenServiceDep,
) -> list[schemas.CourierRead] | schemas.CourierRead:

    return await
    stmt = select(Courier).options(selectinload(Courier.districts))

    if courier is not None:
        stmt = stmt.where(Courier.id == courier)

    result = await db.execute(stmt)
    couriers = result.scalars().all()

    if not couriers:
        raise HTTPException(status_code=404, detail='Курьер не найден')

    return [CourierRead.model_validate(courier) for courier in couriers]


@router.post('/couriers', response_model=CourierRegisterResponse)
async def add_courier(courier: CourierRegister, db: AsyncSessionLocal = Depends(get_session)):
    try:
        stmt = select(District).where(District.name.in_(courier.districts))
        result = await db.execute(stmt)
        districts = result.scalars().all()

        if len(districts) != len(set(courier.districts)):
            raise HTTPException(status_code=400, detail="Некоторые районы не найдены")

        new_courier = Courier(name=courier.name)
        new_courier.districts = districts

        db.add(new_courier)
        await db.commit()
        await db.refresh(new_courier)

        stmt = (
            select(Courier)
            .options(selectinload(Courier.districts))
            .where(Courier.id == new_courier.id)
        )
        result = await db.execute(stmt)
        courier_with_districts = result.scalar_one()

        return courier_with_districts

    except Exception as e:
        await db.rollback()
        return f'Ошибка добавления {str(e)}'
