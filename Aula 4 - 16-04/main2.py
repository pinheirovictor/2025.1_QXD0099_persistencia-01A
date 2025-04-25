from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    nome: str
    valor: float
    is_oferta: Union[bool, None] = None
    
items_db = {}

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.put("/items/{item_id}")
def atualiza_item(item_id: int, item: Item):
    items_db[item_id] = item
    return {"mensagem": "Item atualizado com sucesso"}

@app.get("/itens")
def ler_item():
    return {"itens": items_db.items()}