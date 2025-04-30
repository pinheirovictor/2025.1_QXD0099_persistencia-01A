from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import json
from pathlib import Path
from logger import logger

app = FastAPI()

PASTA_DADOS = Path("dados")
PASTA_DADOS.mkdir(exist_ok=True)

ARQUIVO_AUTORES = PASTA_DADOS / "autores.json"
ARQUIVO_LIVROS = PASTA_DADOS / "livros.jon"

for arquivo in [ARQUIVO_AUTORES, ARQUIVO_LIVROS]:
    if not arquivo.exists():
        arquivo.write_text("[]")

class Autor(BaseModel):
    id: int
    nome: str
    
class Livro(BaseModel):
    id: int
    titulo: str
    autor_id: int
    

def ler_json(arquivo: Path):
    return json.loads(arquivo.read_text())

def escrever_json(arquivo: Path, dados):
    arquivo.write_text(json.dumps(dados, indent=4))
    
@app.post("/autores/", response_model=Autor)
def criar_autor(autor: Autor):
    autores = ler_json(ARQUIVO_AUTORES)
    if any(a["id"] == autor.id for a in autores):
        raise HTTPException(status_code=400, detail="ID já cadastrado")
    autores.append(autor.model_dump())
    escrever_json(ARQUIVO_AUTORES, autores)
    logger.info(f"Autor criado: {autor}")
    return autor

@app.get("/autores/", response_model=List[Autor])
def listar_autores():
    return ler_json(ARQUIVO_AUTORES)

@app.put("/autores/{autor_id}", response_model=Autor)
def atualizar_autor(autor_id: int, autor_atualizado: Autor):
    autores = ler_json(ARQUIVO_AUTORES)
    for idx, a in enumerate(autores):
        if a["id"] == autor_id:
            autores[idx] = autor_atualizado.model_dump
            escrever_json(ARQUIVO_AUTORES, autores)
            logger.info(f"Autor atualizado: {autor_atualizado}")
            return autor_atualizado
    raise HTTPException(status_code=404, detail="Autor não encontrado")

@app.delete("/autores/{autor_id}")
def deletar_autor(autor_id: int):
    autores = ler_json(ARQUIVO_AUTORES)
    autores = [a for a in autores if a["id"] != autor_id]
    escrever_json(ARQUIVO_AUTORES, autores)
    logger.info(f"Autor deletado com sucesso: {autor_id}")
    return {"detail":"Autor deletado"}


@app.post("/livros/", response_model=Livro)
def criar_livro(livro: Livro):
    autores = ler_json(ARQUIVO_AUTORES)
    if not any(a["id"] == livro.autor_id for a in autores):
        raise HTTPException(status_code=400, detail="Autor não encontrado")
    
    livros = ler_json(ARQUIVO_LIVROS)
    if any(l["id"] == livro.id for l in livro):
        raise HTTPException(status_code=400, detail="Id do livro já cadastrado")
    
    livros.append(livro.model_dump)
    escrever_json(ARQUIVO_LIVROS, livros)
    logger.info(f"Livro criado: {livro}")
    return livro

@app.get("/livros/", response_model=List[Livro])
def listar_livros():
    return ler_json(ARQUIVO_LIVROS)

@app.put("/livros/{livro_id}", response_model=Livro)
def atualizar_livro(livro_id: int, livro_atualizado: Livro):
    livros = ler_json(ARQUIVO_LIVROS)
    for idx, l in enumerate(livros):
        if l["id"] == livro_id:
            livros[idx] = livro_atualizado.model_dump()
            escrever_json(ARQUIVO_LIVROS, livros)
            logger.info(f"Livro atualizado: {livro_atualizado}")
            return livro_atualizado
    raise HTTPException(status_code=404, detail="Livro não encontrado.")

# Deleta um livro
@app.delete("/livros/{livro_id}")
def deletar_livro(livro_id: int):
    livros = ler_json(ARQUIVO_LIVROS)
    livros = [l for l in livros if l["id"] != livro_id]
    escrever_json(ARQUIVO_LIVROS, livros)
    logger.info(f"Livro deletado: {livro_id}")
    return {"detail": "Livro deletado"}


@app.get("/autores/{autor_id}/livros", response_model=List[Livro])
def obter_livros_por_autor(autor_id: int):
    autores = ler_json(ARQUIVO_AUTORES)
    if not any(a["id"] == autor_id for a in autores):
        raise HTTPException(status_code=404, detail="autor não encontrado")
    
    livros = ler_json(ARQUIVO_LIVROS)
    livros_autor = [l for l in livros if l["autor_id"] == autor_id]
    logger.info(f"Livros recuperados para o autor: {autor_id}: {livros_autor}")
    return livros_autor
    

