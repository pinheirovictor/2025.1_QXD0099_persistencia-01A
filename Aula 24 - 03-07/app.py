from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table
from cassandra.cqlengine.query import DoesNotExist
from cassandra.cluster import Cluster
import time
from typing import List

from models import Aluno, Disciplina, AlunoDisciplina

def cria_keyspace_escola():
    cluster = Cluster(['127.0.0.1'])
    session = cluster.connect()
    session.execute("""
        CREATE KEYSPACE IF NOT EXISTS escola
        WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 };
    """)
    session.shutdown()
    cluster.shutdown()

# ----- SCHEMAS Pydantic -----

class AlunoIn(BaseModel):
    matricula: str
    nome: str
    curso: str
    ano: int

class AlunoOut(AlunoIn):
    pass

class DisciplinaIn(BaseModel):
    codigo: str
    nome: str
    professor: str

class DisciplinaOut(DisciplinaIn):
    pass

class AlunoDisciplinaIn(BaseModel):
    matricula: str
    codigo_disciplina: str

class AlunoDisciplinaOut(AlunoDisciplinaIn):
    pass

# ----- APP -----

app = FastAPI(title="CRUD Cassandra + FastAPI + ORM (CQLengine) - Alunos e Disciplinas")

@app.on_event("startup")
def startup():
    cria_keyspace_escola()
    time.sleep(1)
    connection.setup(['127.0.0.1'], "escola", protocol_version=3)
    sync_table(Aluno)
    sync_table(Disciplina)
    sync_table(AlunoDisciplina)

# ----- CRUD Aluno -----

@app.post("/alunos/", response_model=AlunoOut)
def criar_aluno(aluno: AlunoIn):
    try:
        obj = Aluno.create(**aluno.dict())
        return AlunoOut(**dict(obj))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/alunos/{matricula}", response_model=AlunoOut)
def obter_aluno(matricula: str):
    try:
        aluno = Aluno.get(matricula=matricula)
        return AlunoOut(**dict(aluno))
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")

@app.get("/alunos/get", response_model=list[AlunoOut])
def listar_alunos():
    return [AlunoOut(**dict(a)) for a in Aluno.all()]


@app.get("/alunos/", response_model=List[AlunoOut])
def listar_alunos(page: int = Query(1, gt=0), page_size: int = Query(10, gt=0, le=100)):
    # Calcular o início da página
    offset = (page - 1) * page_size
    # O método .all() retorna um QuerySet. Você pode fatiar em memória:
    alunos = list(Aluno.all())
    paginados = alunos[offset:offset+page_size]
    return [AlunoOut(**dict(a)) for a in paginados]

@app.put("/alunos/{matricula}", response_model=AlunoOut)
def atualizar_aluno(matricula: str, dados: AlunoIn):
    try:
        aluno = Aluno.get(matricula=matricula)
        aluno.update(**dados.dict())
        aluno_atualizado = Aluno.get(matricula=matricula)
        return AlunoOut(**dict(aluno_atualizado))
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")

@app.delete("/alunos/{matricula}")
def deletar_aluno(matricula: str):
    try:
        aluno = Aluno.get(matricula=matricula)
        aluno.delete()
        return {"detail": "Aluno removido com sucesso"}
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")

# ----- CRUD Disciplina -----

@app.post("/disciplinas/", response_model=DisciplinaOut)
def criar_disciplina(disciplina: DisciplinaIn):
    try:
        obj = Disciplina.create(**disciplina.dict())
        return DisciplinaOut(**dict(obj))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/disciplinas/{codigo}", response_model=DisciplinaOut)
def obter_disciplina(codigo: str):
    try:
        disciplina = Disciplina.get(codigo=codigo)
        return DisciplinaOut(**dict(disciplina))
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Disciplina não encontrada")

@app.get("/disciplinas/", response_model=list[DisciplinaOut])
def listar_disciplinas():
    return [DisciplinaOut(**dict(d)) for d in Disciplina.all()]

@app.delete("/disciplinas/{codigo}")
def deletar_disciplina(codigo: str):
    try:
        disciplina = Disciplina.get(codigo=codigo)
        disciplina.delete()
        return {"detail": "Disciplina removida com sucesso"}
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Disciplina não encontrada")

# ----- Associação Aluno <-> Disciplina (N:N) -----

@app.post("/alunos/{matricula}/disciplinas/{codigo_disciplina}", response_model=AlunoDisciplinaOut)
def matricular_aluno_disciplina(matricula: str, codigo_disciplina: str):
    # Validação: aluno e disciplina existem?
    try:
        Aluno.get(matricula=matricula)
        Disciplina.get(codigo=codigo_disciplina)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Aluno ou disciplina não encontrado")
    obj = AlunoDisciplina.create(matricula=matricula, codigo_disciplina=codigo_disciplina)
    return AlunoDisciplinaOut(**dict(obj))

@app.get("/alunos/{matricula}/disciplinas/", response_model=list[DisciplinaOut])
def listar_disciplinas_do_aluno(matricula: str):
    associations = AlunoDisciplina.filter(matricula=matricula)
    codigos = [a.codigo_disciplina for a in associations]
    if not codigos:
        return []
    return [DisciplinaOut(**dict(d)) for d in Disciplina.objects.filter(codigo__in=codigos)]

# @app.get("/disciplinas/{codigo}/alunos/", response_model=list[AlunoOut])
# def listar_alunos_na_disciplina(codigo: str):
#     associations = AlunoDisciplina.filter(codigo_disciplina=codigo)
#     matriculas = [a.matricula for a in associations]
#     if not matriculas:
#         return []
#     return [AlunoOut(**dict(a)) for a in Aluno.objects.filter(matricula__in=matriculas)]

# @app.delete("/alunos/{matricula}/disciplinas/{codigo_disciplina}")
# def remover_aluno_disciplina(matricula: str, codigo_disciplina: str):
#     obj = AlunoDisciplina.filter(matricula=matricula, codigo_disciplina=codigo_disciplina).first()
#     if obj:
#         obj.delete()
#         return {"detail": "Associação removida"}
#     raise HTTPException(status_code=404, detail="Associação não encontrada")
