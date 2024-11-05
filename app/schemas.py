from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.orm.models import OrderStatus, CurrencyType


class OrderCreateUpdateSchema(BaseModel):
    customer_name: str
    order_date: datetime
    status: OrderStatus
    total_amount: float
    currency: CurrencyType

    class Config:
        orm_mode = True
        from_attributes = True


class OrderSchema(OrderCreateUpdateSchema):
    id: int


class OrderSchemaWithConvertedAmount(OrderSchema):
    converted_amount: Optional[float] = 0
