import psycopg2
from psycopg2.extras import RealDictCursor

def get_connection():
    return psycopg2.connect(
        database="db3",
        user="postgres",
        password="2023",
        host="localhost",
        port="5432"
    )

# CRUD para Usuário
def create_usuario(nome: str, email: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO usuario (nome, email) VALUES (%s, %s) RETURNING id", (nome, email))
    user_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return user_id

def list_usuarios():
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM usuario")
    usuarios = cursor.fetchall()
    cursor.close()
    conn.close()
    return usuarios


# CRUD para Produto
def create_produto(nome: str, preco: float):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO produto (nome, preco) VALUES (%s, %s) RETURNING id",
        (nome, preco)
    )
    produto_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return produto_id

def list_produtos():
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM produto")
    produtos = cursor.fetchall()
    cursor.close()
    conn.close()
    return produtos

# CRUD para Pedido
def create_pedido(usuario_id: int, data_pedido: str, status: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO pedido (usuario_id, data_pedido, status) VALUES (%s, %s, %s) RETURNING id",
        (usuario_id, data_pedido, status)
    )
    pedido_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return pedido_id

def list_pedidos():
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM pedido")
    pedidos = cursor.fetchall()
    cursor.close()
    conn.close()
    return pedidos

# CRUD para PedidoProduto (associação entre Pedido e Produto)
def add_produto_pedido(pedido_id: int, produto_id: int, quantidade: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO pedido_produto (pedido_id, produto_id, quantidade) VALUES (%s, %s, %s)",
        (pedido_id, produto_id, quantidade)
    )
    conn.commit()
    cursor.close()
    conn.close()

def list_pedido_produtos(pedido_id: int):
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute(
        """
        SELECT pp.pedido_id, pp.produto_id, p.nome as produto_nome, p.preco, pp.quantidade
        FROM pedido_produto pp
        JOIN produto p ON pp.produto_id = p.id
        WHERE pp.pedido_id = %s
        """,
        (pedido_id,)
    )
    pedido_produtos = cursor.fetchall()
    cursor.close()
    conn.close()
    return pedido_produtos

