import json
from typing import Optional, Any, List

from fastapi import FastAPI, HTTPException, status, Path, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from datetime import datetime

import logging

from sanic.response import JSONResponse

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI()


# Models (schemas)
class Product(BaseModel):
    id: Optional[int] = Field(None, description="The ID of the product")
    name: str
    type: str
    inventory: int
    cost: float


class ProductId(BaseModel):
    id: int


class Order(BaseModel):
    id: Optional[int] = Field(None, description="The ID of the order")
    productid: int
    count: int
    status: str


class OrderId(BaseModel):
    id: int


class ErrorResponse(BaseModel):
    timestamp: str
    status: int
    error: str
    message: str
    path: str


def custom_encoder(obj: Any) -> Any:
    if isinstance(obj, ErrorResponse):
        return jsonable_encoder(obj.dict())
    return obj


# In-memory data stores
products = {}
orders = {}


# Helper functions
def current_time():
    return datetime.utcnow().isoformat() + "Z"


# Product Endpoints
@app.get("/products/{id}", response_model=Any)
async def get_product(id: int = Path(..., example=10)):
    product = products.get(id)
    if not product:
        print("C")
        response = ErrorResponse(timestamp=current_time(), status=404, error="Not Found", message="",
                                 path=f"/products/{id}", )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=response.__dict__,
        )
    print("D")
    return product


@app.post("/products/{id}", response_model=str)
async def update_product(id: int, product: Product):
    products[id] = product
    return "success"


@app.post("/products", status_code=201)
async def push_product(product: Product):
    index = 0
    while index in products:
        index += 1
    product.id = index
    products[index] = product
    print(ProductId(id=product.id).dict())
    return {"id":product.id}


@app.delete("/products/{id}", response_model=str)
async def delete_product(id: int):
    logger.info("b")
    print("b ")
    if id in products:
        del products[id]
        return ""
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad Request")


@app.get("/products", response_model=List[Product])
async def search_products(name: Optional[str] = Query(None), type: Optional[str] = Query(None)):
    result = []
    for product in products.values():
        if name and name not in product.name:
            continue
        if type and type != product.type:
            continue
        result.append(product)
    return result


# Order Endpoints
@app.post("/orders", response_model=OrderId)
async def create_order(order: Order):
    order.id = len(orders) + 1
    orders[order.id] = order
    return OrderId(id=order.id)


@app.get("/orders", response_model=List[Order])
async def search_orders(productid: Optional[int] = Query(None), status: Optional[str] = Query(None)):
    result = []
    for order in orders.values():
        if productid and order.productid != productid:
            continue
        if status and order.status != status:
            continue
        result.append(order)
    return result


@app.get("/orders/{id}", response_model=Order)
async def get_order(id: int = Path(..., example=10)):
    order = orders.get(id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ErrorResponse(
            timestamp=current_time(), status=404, error="Not Found", path=f"/orders/{id}"))
    return order


@app.post("/orders/{id}", response_model=str)
async def update_order(id: int, order: Order):
    if id not in orders:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad Request")
    orders[id] = order
    return ""


@app.delete("/orders/{id}", response_model=str)
async def delete_order(id: int):
    if id in orders:
        del orders[id]
        return ""
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad Request")
