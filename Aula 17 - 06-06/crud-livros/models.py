from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

class Livro(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    titulo: str
    ano: int
    autor_id: int = Field(foreign_key="autor.id")
    autor: Optional["Autor"] = Relationship(back_populates="livros")  # <--- ADICIONE ESSA LINHA!

class Autor(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    #pode comentar
    email: Optional[str] = Field(default=None, index=True)
    livros: List["Livro"] = Relationship(back_populates="autor")

Livro.update_forward_refs()
