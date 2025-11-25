from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column

from sqlalchemy.orm import relationship

from app.core.database import Base
from .statuses_enum import StatusEnum

if TYPE_CHECKING:
    from ..courier import Courier
    from ..district import District


class Order(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100))
    status: Mapped[StatusEnum] = mapped_column(comment="Статус заказа")

    created_time: Mapped[datetime] = mapped_column(DateTime())
    completed_time: Mapped[datetime | None] = mapped_column(DateTime())

    district_id: Mapped[int] = mapped_column(ForeignKey('districts.id'))
    courier_id: Mapped[int] = mapped_column(ForeignKey('couriers.id'))

    courier: Mapped["Courier"] = relationship(
        'Courier',
        back_populates='order',
        foreign_keys='Order.courier_id'
    )
    district: Mapped["District"] = relationship(
        'District',
        back_populates='orders',
        foreign_keys='Order.district_id'
    )

    def __repr__(self):
        return f"Заказ №{self.id}, район {self.district.name}"
