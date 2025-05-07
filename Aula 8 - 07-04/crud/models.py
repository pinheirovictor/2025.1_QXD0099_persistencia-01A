from pydantic import BaseModel

class Usuario(BaseModel):
    id: int
    nome: str
    email: str

class Pedido(BaseModel):
    id: int
    usuario_id: int
    data_pedido: str
    status: str

class Produto(BaseModel):
    id: int
    nome: str
    preco: float

class PedidoProduto(BaseModel):
    pedido_id: int
    produto_id: int
    quantidade: int
