from sqlalchemy import Column, Integer, String, Enum as SQLEnum, Float, DateTime
from datetime import datetime
from app.orm.database import Base
from enum import Enum


class OrderStatus(Enum):
    PENDING = "pending"
    SHIPPED = "shipped"
    DELIVERED = "delivered"


class CurrencyType(Enum):
    USD = "USD"
    EUR = "EUR"


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String, nullable=False)
    order_date = Column(DateTime, default=datetime.utcnow)
    currency = Column(SQLEnum(CurrencyType), default=CurrencyType.USD)
    status = Column(SQLEnum(OrderStatus), default=OrderStatus.PENDING)
    total_amount = Column(Float, nullable=False)
