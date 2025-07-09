from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import redis
from typing import List, Optional

app = FastAPI()
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# Modelos Pydantic
class Usuario(BaseModel):
    nome: str
    idade: int

class UsuarioUpdate(BaseModel):
    nome: Optional[str] = None
    idade: Optional[int] = None

class Tarefa(BaseModel):
    tarefa: str

# --- Usuário CRUD ---

# Criar usuário
@app.post("/usuarios/{user_id}")
def cria_usuario(user_id: int, usuario: Usuario):
    key = f"user:{user_id}"
    if r.exists(key):
        raise HTTPException(status_code=409, detail="Usuário já existe")
    r.hset(key, mapping=usuario.dict())
    r.sadd("usuarios", user_id)  # Salva o ID em um set global
    return {"msg": "Usuário cadastrado"}

# Consultar usuário
@app.get("/usuarios/{user_id}")
def consulta_usuario(user_id: int):
    key = f"user:{user_id}"
    usuario = r.hgetall(key)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario

# Atualizar usuário
@app.put("/usuarios/{user_id}")
def atualiza_usuario(user_id: int, usuario: UsuarioUpdate):
    key = f"user:{user_id}"
    if not r.exists(key):
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    dados = {k: v for k, v in usuario.dict().items() if v is not None}
    if not dados:
        raise HTTPException(status_code=400, detail="Nada para atualizar")
    r.hset(key, mapping=dados)
    return {"msg": "Usuário atualizado"}

# Deletar usuário
@app.delete("/usuarios/{user_id}")
def deleta_usuario(user_id: int):
    key = f"user:{user_id}"
    if not r.exists(key):
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    r.delete(key)
    r.srem("usuarios", user_id)
    # Remove tarefas associadas
    r.delete(f"tarefas:{user_id}")
    return {"msg": "Usuário removido"}

# Listar todos os usuários
@app.get("/usuarios/")
def lista_usuarios():
    user_ids = r.smembers("usuarios")
    usuarios = []
    for user_id in user_ids:
        data = r.hgetall(f"user:{user_id}")
        if data:
            data['id'] = user_id
            usuarios.append(data)
    return usuarios

# --- Tarefas CRUD ---

# Adicionar tarefa
@app.post("/tarefas/{user_id}")
def cria_tarefa(user_id: int, tarefa: Tarefa):
    if not r.exists(f"user:{user_id}"):
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    r.rpush(f"tarefas:{user_id}", tarefa.tarefa)
    return {"msg": "Tarefa adicionada"}

# Listar tarefas
@app.get("/tarefas/{user_id}")
def lista_tarefas(user_id: int):
    if not r.exists(f"user:{user_id}"):
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    tarefas = r.lrange(f"tarefas:{user_id}", 0, -1)
    return {"tarefas": tarefas}

# Atualizar tarefa por índice
@app.put("/tarefas/{user_id}/{index}")
def atualiza_tarefa(user_id: int, index: int, tarefa: Tarefa):
    key = f"tarefas:{user_id}"
    if not r.exists(key):
        raise HTTPException(status_code=404, detail="Usuário ou tarefas não encontrados")
    tamanho = r.llen(key)
    if index < 0 or index >= tamanho:
        raise HTTPException(status_code=400, detail="Índice fora do intervalo")
    r.lset(key, index, tarefa.tarefa)
    return {"msg": "Tarefa atualizada"}

# Deletar tarefa por índice
@app.delete("/tarefas/{user_id}/{index}")
def deletar_tarefa(user_id: int, index: int):
    key = f"tarefas:{user_id}"
    if not r.exists(key):
        raise HTTPException(status_code=404, detail="Usuário ou tarefas não encontrados")
    tarefas = r.lrange(key, 0, -1)
    if index < 0 or index >= len(tarefas):
        raise HTTPException(status_code=400, detail="Índice fora do intervalo")
    valor = tarefas[index]
    # Remove apenas a primeira ocorrência do valor
    r.lrem(key, 1, valor)
    return {"msg": "Tarefa removida"}

# Listar todas as tarefas de todos os usuários (extra)
@app.get("/tarefas/")
def listar_todas_tarefas():
    user_ids = r.smembers("usuarios")
    todas = {}
    for user_id in user_ids:
        tarefas = r.lrange(f"tarefas:{user_id}", 0, -1)
        todas[user_id] = tarefas
    return todas
