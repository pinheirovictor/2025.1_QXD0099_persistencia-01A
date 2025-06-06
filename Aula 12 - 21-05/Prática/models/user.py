from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
# from .profile import Profile
# from .product import Product
# from .order import Order

class UserBase(SQLModel):
    nome: str
    email: str

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    profile: Optional["Profile"] = Relationship(back_populates="user")
    produtos: List["Product"] = Relationship(back_populates="vendedor")
    pedidos: List["Order"] = Relationship(back_populates="comprador")

class UserRead(UserBase):
    id: int

class UserCreate(UserBase):
    pass
