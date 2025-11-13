from sqlalchemy import Column, Integer, String, ForeignKey, JSON, Float, DateTime
from datetime import datetime

from sqlalchemy.orm import relationship

from app.core.database import Base


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)

    created_time = Column(DateTime, default=datetime.utcnow)
    completed_time = Column(DateTime, nullable=True)

    status_id = Column(Integer, ForeignKey('order_statuses.id'))
    district_id = Column(Integer, ForeignKey('districts.id'))
    courier_id = Column(Integer, ForeignKey('couriers.id'))

    status = relationship('OrderStatus', back_populates='orders', foreign_keys='Order.status_id')
    courier = relationship('Courier', back_populates='orders', foreign_keys='Order.courier_id')
    district = relationship('District', back_populates='orders', foreign_keys='Order.district_id')

    def __repr__(self):
        return f"Заказ №{self.id}, район {self.district.name}"


class OrderStatus(Base):
    __tablename__ = 'order_statuses'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)

    orders = relationship('Order', back_populates='status')

    def __repr__(self):
        return f"Статус заказа №{self.orders.name} {self.name}"


