





from fastapi import FastAPI
from routes import professores, alunos

app = FastAPI()

app.include_router(professores.router)
app.include_router(alunos.router)