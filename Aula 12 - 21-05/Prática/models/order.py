from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
# from .user import User
# from .order_product import OrderProduct

class OrderBase(SQLModel):
    data: str
    status: str

class Order(OrderBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    comprador_id: int = Field(foreign_key="user.id")
    comprador: Optional["User"] = Relationship(back_populates="pedidos")
    produtos: List["OrderProduct"] = Relationship(back_populates="pedido")

class OrderRead(OrderBase):
    id: int
    comprador_id: int

class OrderCreate(OrderBase):
    comprador_id: int
