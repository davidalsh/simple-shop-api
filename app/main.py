from fastapi import FastAPI, Depends
from app.orm.database import engine, Base
from app.orm.models import OrderStatus
from app.orm.repositories.order import OrderRepository
from app.schemas import OrderSchema, OrderCreateUpdateSchema, OrderSchemaWithConvertedAmount


Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/orders", response_model=list[OrderSchemaWithConvertedAmount])
def list_orders(
    skip: int = 0,
    limit: int = 100,
    status: OrderStatus | None = None,
    repository: OrderRepository = Depends(OrderRepository.create_session),
):
    orders = repository.list_orders(
        status=status,
        skip=skip,
        limit=limit,
    )
    return repository.get_order_schema_with_converted_amount(orders)


@app.get("/orders/{order_id}", response_model=OrderSchemaWithConvertedAmount)
def get_order(order_id: int, repository: OrderRepository = Depends(OrderRepository.create_session)):
    order = repository.get_order(order_id)
    return repository.get_order_schema_with_converted_amount([order])[0]


@app.post("/orders", response_model=OrderSchema, status_code=201)
def create_order(order: OrderCreateUpdateSchema, repository: OrderRepository = Depends(OrderRepository.create_session)):
    return repository.create_order(order)


@app.put("/orders/{order_id}", response_model=OrderSchema)
def update_order(
    order_id: int,
    order: OrderCreateUpdateSchema,
    repository: OrderRepository = Depends(OrderRepository.create_session),
):
    return repository.update_order(order_id, order)


@app.delete("/orders/{order_id}", status_code=204)
def delete_order(order_id: int, repository: OrderRepository = Depends(OrderRepository.create_session)):
    repository.delete_order(order_id)
