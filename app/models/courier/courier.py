from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB, INTERVAL
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from ..associations import courier_districts

from app.core.database import Base
from ..user import User
from ..order import Order


class Courier(Base):
    __tablename__ = 'couriers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    active_order = Column(JSONB, nullable=True)
    avg_order_complete_time = Column(INTERVAL)
    avg_day_orders = Column(Float)

    register_at = Column(DateTime, default=datetime.utcnow)

    user_sid: Mapped["User"] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        comment="SID of user"
    )
    orders: Mapped[list["Order"]]= relationship('Order', back_populates='courier')
    districts = relationship("District",
                             secondary=courier_districts,
                             back_populates="couriers",
                             lazy='selectin'
    )
    user: Mapped["User"] = relationship(
        back_populates="courier"
    )

    def __repr__(self):
        return f"Курьер {self.user.username}"


