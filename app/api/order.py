from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, and_
from typing import Optional, List

from sqlalchemy.orm import selectinload

from app.models import Order, District, Courier
from app.models.order import OrderStatus
from app.schemas.courier import CourierRead, CourierBase
from app.schemas.order import OrderCreate, OrderWithCourier, OrderCreateResponse, OrderRead
from app.core.database import get_session, AsyncSessionLocal
from app.utils.courier import get_courier_stats_by_orders

router = APIRouter()


@router.get('/orders', response_model=List[OrderWithCourier])
async def get_orders(order: Optional[int] = None, db: AsyncSessionLocal = Depends(get_session)):
    stmt = select(Order).options(selectinload(Order.courier))

    if order is not None:
        stmt = stmt.where(Order.id == order)

    result = await db.execute(stmt)
    orders = result.scalars().all()

    if not orders:
        raise HTTPException(status_code=404, detail="Заказ не найден")

    return [OrderWithCourier.model_validate(order) for order in orders]


@router.post('/orders', response_model=OrderCreateResponse)
async def add_order(order: OrderCreate, db: AsyncSessionLocal = Depends(get_session)):
    try:
        result = await db.execute(select(District).where(District.name == order.district))
        district = result.scalar_one_or_none()
        if not district:
            raise HTTPException(status_code=404, detail="Район не найден")

        result = await db.execute(
            select(Courier)
            .join(Courier.districts)
            .where(and_(
                District.id == district.id,
                Courier.active_order.is_(None))
            )
            .limit(1)
        )

        courier = result.scalars().first()
        if not courier:
            raise HTTPException(status_code=404, detail="Нет свободных курьеров в этом районе")

        new_order = Order(
            name=order.name,
            district_id=district.id,
            courier_id=courier.id,
            status_id=1
        )

        db.add(new_order)
        await db.commit()
        await db.refresh(new_order)

        courier.active_order = {
            'id': new_order.id,
            'name': new_order.name
        }

        db.add(courier)
        await db.commit()
        await db.refresh(courier)

        order_data = OrderRead.model_validate(new_order)
        courier_data = CourierBase.model_validate(courier)

        return OrderCreateResponse(**order_data.model_dump(), courier=courier_data)

    except Exception as e:
        await db.rollback()
        return f'Ошибка добавления {str(e)}'


@router.patch('/orders/{order_id}/complete', response_model=OrderWithCourier)
async def complete_order(order_id: int, db: AsyncSessionLocal = Depends(get_session)):
    try:
        # Получение заказа
        result = await db.execute(select(Order).where(Order.id == order_id))
        order = result.scalar_one_or_none()

        if not order:
            raise HTTPException(status_code=404, detail="Заказ не найден")

        if not order.courier_id:
            raise HTTPException(status_code=400, detail="У заказа нет курьера")

        # Получение курьера
        result = await db.execute(select(Courier).where(Courier.id == order.courier_id))
        courier = result.scalar_one_or_none()

        if not courier:
            raise HTTPException(status_code=404, detail="Курьер не найден")

        if courier.active_order is None or courier.active_order.get('id') != order.id:
            raise HTTPException(status_code=400, detail="Этот заказ не активен у курьера")

        result = await db.execute(select(OrderStatus).where(OrderStatus.name == 'Завершен'))
        order_status = result.scalar_one_or_none()

        order.completed_time = datetime.utcnow()
        order.status_id = order_status.id

        courier.active_order = None

        await get_courier_stats_by_orders(db, courier.id)

        await db.commit()
        await db.refresh(order)

        return OrderWithCourier.model_validate(order)

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка завершения заказа: {str(e)}")

