from sqlmodel import SQLModel, Field, Relationship
from typing import Optional


class ProfileBase(SQLModel):
    endereco: str
    telefone: str

class Profile(ProfileBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", unique=True)
    user: Optional["User"] = Relationship(back_populates="profile")

class ProfileRead(ProfileBase):
    id: int
    user_id: int

class ProfileCreate(ProfileBase):
    user_id: int
