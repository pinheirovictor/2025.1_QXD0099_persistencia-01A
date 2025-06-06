from fastapi import FastAPI, Request, Response
from core.database import create_db_and_tables
from core.logging_config import setup_logging
from routers import user, profile, product, order, order_product, advanced


# pip install "pydantic<2.0.0" "sqlmodel<0.0.9" "fastapi<0.110"

app = FastAPI()

# Configuração de logs
setup_logging()

# Criação do banco/tabelas no startup
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Registro dos routers CRUD e avançados
app.include_router(user)
app.include_router(profile)
app.include_router(product)
app.include_router(order)
app.include_router(order_product)
app.include_router(advanced)


# Middleware de logging para todas as requisições
@app.middleware("http")
async def log_middleware(request: Request, call_next):
    response = await call_next(request)
    from utils.logger import log_request
    log_request(request, response)
    return response
