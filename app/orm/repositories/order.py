from dataclasses import dataclass

from app.npb_client import NPBApiClient
from app.orm.database import SessionLocal
from app.orm.dependencies import get_db
from fastapi import Depends

from app.exceptions import DetailNotFound
from app.orm.models import Order, OrderStatus
from app.orm.database import Base
from app.schemas import OrderCreateUpdateSchema, OrderSchemaWithConvertedAmount


@dataclass
class OrderRepository:
    db_session: SessionLocal
    api_client: NPBApiClient

    @classmethod
    def create_session(cls, session: SessionLocal = Depends(get_db)):
        return cls(db_session=session, api_client=NPBApiClient())

    @property
    def model(self) -> Base:
        return Order

    def get_one_or_notfound(self, order_id):
        order = self.db_session.query(self.model).filter(self.model.id == order_id).first()
        if not order:
            raise DetailNotFound("Order")
        return order

    def get_order_schema_with_converted_amount(self, orders: list[Order]) -> list[OrderSchemaWithConvertedAmount]:
        order_schemas = []
        for order in orders:
            order_schema = OrderSchemaWithConvertedAmount.from_orm(order)
            order_schema.converted_amount = self.api_client.convert_to(order.currency, order.total_amount)
            order_schemas.append(order_schema)
        return order_schemas

    def list_orders(self, status: OrderStatus | None, skip: int, limit: int) -> list[Order]:
        query = (
            self.db_session.query(self.model)
        )
        if status:
            query = query.filter(self.model.status == status)
        orders = query.offset(skip).limit(limit).all()
        return orders

    def get_order(self, order_id: int) -> tuple[Order, float]:
        return self.get_one_or_notfound(order_id)

    def create_order(self, order: OrderCreateUpdateSchema):
        try:
            order = self.model(**order.dict())
            self.db_session.add(order)
            self.db_session.commit()
            self.db_session.refresh(order)
        except Exception as exc:
            print(f"An error occurred while creating the order: {order}")
            raise exc
        return order

    def update_order(self, order_id: int, order: OrderCreateUpdateSchema):
        previous_order = self.get_one_or_notfound(order_id)

        for field, value in order.dict().items():
            setattr(previous_order, field, value)

        try:
            self.db_session.commit()
            self.db_session.refresh(previous_order)
        except Exception as exc:
            self.db_session.rollback()
            print(f"An error occurred while updating the order: {order_id}")
            raise exc
        return previous_order

    def delete_order(self, order_id: int):
        order = self.get_one_or_notfound(order_id)
        try:
            self.db_session.delete(order)
            self.db_session.commit()
        except Exception as exc:
            self.db_session.rollback()
            print(f"An error occurred while deleting the order: {order_id}")
            raise exc
