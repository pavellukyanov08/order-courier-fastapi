from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import JSONB, INTERVAL
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from app.core.database import Base
from ..associations import courier_districts

if TYPE_CHECKING:
    from ..order import Order
    from ..district import District
    from app.common.models import User


class Courier(Base):
    __tablename__ = 'couriers'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    active_order: Mapped[dict | None] = mapped_column(JSONB)
    avg_order_complete_time: Mapped[float | None] = mapped_column(INTERVAL)
    avg_day_orders: Mapped[float | None] = mapped_column()

    register_at: Mapped[datetime] = mapped_column(DateTime())

    user_sid: Mapped[UUID] = mapped_column(
        ForeignKey("user.sid", ondelete="CASCADE"),
        index=True,
        comment="SID of user"
    )
    districts: Mapped[list["District"]] = relationship(
        "District",
        back_populates='couriers',
        secondary=courier_districts,
        lazy='selectin'
    )
    order: Mapped["Order"] = relationship('Order', back_populates='courier')
    user: Mapped["User"] = relationship("User", back_populates="courier")

    def __repr__(self):
        return f"Курьер {self.user.username}"


