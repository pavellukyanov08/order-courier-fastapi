from sqlalchemy.orm import relationship, mapped_column, Mapped
from ..associations import courier_districts

from app.core.database import Base
from ..courier import Courier
from ..order import Order


class District(Base):
    __tablename__ = 'districts'

    id: Mapped[id] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)

    couriers: Mapped[list["Courier"]] = relationship(
        "Courier",
        back_populates="districts",
        secondary=courier_districts
    )
    orders: Mapped[list["Order"]] = relationship(
        "Order",
        back_populates="district"
    )

    def __repr__(self):
        return f"Район {self.name}"


