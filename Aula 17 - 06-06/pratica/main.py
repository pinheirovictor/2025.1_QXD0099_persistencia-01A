from fastapi import FastAPI, Depends
from sqlmodel import Session, select
from database import engine
from models import Autor, Livro, SQLModel  # Adicione SQLModel

# Criação automática das tabelas (só executa se não existirem)
SQLModel.metadata.create_all(engine)

app = FastAPI()

def get_session():
    with Session(engine) as session:
        yield session

@app.post("/autores/", response_model=Autor)
def criar_autor(autor: Autor, session: Session = Depends(get_session)):
    session.add(autor)
    session.commit()
    session.refresh(autor)
    return autor

@app.get("/autores/", response_model=list[Autor])
def listar_autores(session: Session = Depends(get_session)):
    return session.exec(select(Autor)).all()
