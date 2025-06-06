from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
# from .order import Order
# from .product import Product

class OrderProductBase(SQLModel):
    quantidade: int

class OrderProduct(OrderProductBase, table=True):
    order_id: int = Field(foreign_key="order.id", primary_key=True)
    product_id: int = Field(foreign_key="product.id", primary_key=True)
    pedido: Optional["Order"] = Relationship(back_populates="produtos")
    produto: Optional["Product"] = Relationship(back_populates="pedidos")

class OrderProductRead(OrderProductBase):
    order_id: int
    product_id: int

class OrderProductCreate(OrderProductBase):
    order_id: int
    product_id: int

