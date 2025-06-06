from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
# from .user import User
# from .order_product import OrderProduct

class ProductBase(SQLModel):
    nome: str
    descricao: str
    preco: float

class Product(ProductBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    vendedor_id: int = Field(foreign_key="user.id")
    vendedor: Optional["User"] = Relationship(back_populates="produtos")
    pedidos: List["OrderProduct"] = Relationship(back_populates="produto")

class ProductRead(ProductBase):
    id: int
    vendedor_id: int

class ProductCreate(ProductBase):
    vendedor_id: int
