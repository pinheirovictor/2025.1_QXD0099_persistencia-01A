from fastapi import FastAPI
from database import create_db_and_tables
from routers import equipes


app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    
@app.get("/")
def home():
    return {"mensagem": "Bem vindo"}

app.include_router(equipes.router)
