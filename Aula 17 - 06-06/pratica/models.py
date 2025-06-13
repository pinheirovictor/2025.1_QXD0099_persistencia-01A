from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, String

class Autor(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    email: Optional[str] = Field(
        default=None,
        sa_column=Column(String, index=True)  # GARANTE index e tipo correto!
    )
    cpf: Optional[str] = Field(default=None, sa_column=Column(String, unique=True))
    livros: List["Livro"] = Relationship(back_populates="autor")

class Livro(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    titulo: str
    ano: int
    autor_id: int = Field(foreign_key="autor.id")
    autor: Optional["Autor"] = Relationship(back_populates="livros")

Livro.update_forward_refs()
