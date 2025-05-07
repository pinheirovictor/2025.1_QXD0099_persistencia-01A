
from fastapi import FastAPI, HTTPException
from psycopg2.extras import RealDictCursor
from crud import (
    create_usuario, list_usuarios,
    create_produto, list_produtos,
    create_pedido, list_pedidos,
    add_produto_pedido, list_pedido_produtos,
)
from db import get_connection  # você precisa ter o get_connection no db.py

app = FastAPI()

# ------------------------- Usuário -------------------------

@app.post("/usuarios/")
def criar_usuario(nome: str, email: str):
    user_id = create_usuario(nome, email)
    return {"id": user_id, "nome": nome, "email": email}

@app.get("/usuarios/")
def listar_usuarios():
    return list_usuarios()

# ------------------------- Produto -------------------------

@app.post("/produtos/")
def criar_produto(nome: str, preco: float):
    produto_id = create_produto(nome, preco)
    return {"id": produto_id, "nome": nome, "preco": preco}

@app.get("/produtos/")
def listar_produtos():
    return list_produtos()

# ------------------------- Pedido -------------------------

@app.post("/pedidos/")
def criar_pedido(usuario_id: int, data_pedido: str, status: str):
    pedido_id = create_pedido(usuario_id, data_pedido, status)
    return {"id": pedido_id, "usuario_id": usuario_id, "data_pedido": data_pedido, "status": status}

@app.get("/pedidos/")
def listar_pedidos():
    return list_pedidos()

# ------------------------- PedidoProduto -------------------------

@app.post("/pedidos/{pedido_id}/produtos/")
def adicionar_produto_ao_pedido(pedido_id: int, produto_id: int, quantidade: int):
    add_produto_pedido(pedido_id, produto_id, quantidade)
    return {"message": "Produto adicionado ao pedido com sucesso"}

@app.get("/pedidos/{pedido_id}/produtos/")
def listar_produtos_do_pedido(pedido_id: int):
    produtos = list_pedido_produtos(pedido_id)
    return produtos

@app.get("/usuarios_com_pedidos/")
def usuarios_com_pedidos():
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """
        SELECT u.nome, p.id AS pedido_id
        FROM usuario u
        LEFT JOIN pedido p ON u.id = p.usuario_id
    """
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results
