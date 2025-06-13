# Importa o FastAPI para construir a API web
# Depends permite usar injeção de dependências (como o banco de dados)
# HTTPException permite lançar erros HTTP personalizados
from fastapi import FastAPI, Depends, HTTPException

# Importa o tipo Session do SQLAlchemy para interagir com o banco
from sqlalchemy.orm import Session

# Importa os modelos definidos anteriormente
from models import Aluno, Curso, Inscricao

# Importa a função que fornece a sessão do banco de dados
from database import get_db

# Inicializa a aplicação FastAPI
app = FastAPI()

# ------------------------------
# ENDPOINTS PARA ALUNOS
# ------------------------------

# Endpoint POST para criar um novo aluno
@app.post("/alunos")
def criar_aluno(nome: str, email: str, db: Session = Depends(get_db)):
    aluno = Aluno(nome=nome, email=email)  # Cria um objeto Aluno
    db.add(aluno)                          # Adiciona à sessão
    db.commit()                            # Confirma no banco de dados
    db.refresh(aluno)                      # Atualiza o objeto com os dados salvos
    return aluno                           # Retorna o aluno criado

# Endpoint GET para listar todos os alunos
@app.get("/alunos")
def listar_alunos(db: Session = Depends(get_db)):
    return db.query(Aluno).all()  # Retorna todos os alunos

# Endpoint PUT para atualizar um aluno existente
@app.put("/alunos/{aluno_id}")
def atualizar_aluno(aluno_id: int, nome: str, email: str, db: Session = Depends(get_db)):
    aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()  # Busca o aluno

    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")

    aluno.nome = nome      # Atualiza o nome
    aluno.email = email    # Atualiza o email
    db.commit()
    db.refresh(aluno)
    return aluno

# Endpoint DELETE para remover um aluno
@app.delete("/alunos/{aluno_id}")
def deletar_aluno(aluno_id: int, db: Session = Depends(get_db)):
    aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()

    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")

    db.delete(aluno)
    db.commit()
    return {"message": f"Aluno com ID {aluno_id} deletado com sucesso"}

# ------------------------------
# ENDPOINTS PARA CURSOS
# ------------------------------

# Endpoint POST para criar um novo curso
@app.post("/cursos")
def criar_curso(nome: str, descricao: str, db: Session = Depends(get_db)):
    curso = Curso(nome=nome, descricao=descricao)
    db.add(curso)
    db.commit()
    db.refresh(curso)
    return curso

# Endpoint GET para listar todos os cursos
@app.get("/cursos")
def listar_cursos(db: Session = Depends(get_db)):
    return db.query(Curso).all()

# ------------------------------
# ENDPOINTS PARA INSCRIÇÕES
# ------------------------------

# Endpoint POST para inscrever um aluno em um curso
@app.post("/inscricoes")
def criar_inscricao(aluno_id: int, curso_id: int, db: Session = Depends(get_db)):
    # Verifica se o aluno existe
    aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()
    # Verifica se o curso existe
    curso = db.query(Curso).filter(Curso.id == curso_id).first()

    if not aluno or not curso:
        raise HTTPException(status_code=404, detail="Aluno ou Curso não encontrados")

    # Cria a inscrição
    inscricao = Inscricao(aluno_id=aluno_id, curso_id=curso_id)
    db.add(inscricao)
    db.commit()
    db.refresh(inscricao)
    return inscricao

# Endpoint GET para listar todas as inscrições
@app.get("/inscricoes")
def listar_inscricoes(db: Session = Depends(get_db)):
    return db.query(Inscricao).all()


# from fastapi import FastAPI, Depends, HTTPException
# from sqlalchemy.orm import Session
# from models import Aluno, Curso, Inscricao
# from database import get_db

# app = FastAPI()

# # Criar aluno
# @app.post("/alunos")
# def criar_aluno(nome: str, email: str, db: Session = Depends(get_db)):
#     aluno = Aluno(nome=nome, email=email)
#     db.add(aluno)
#     db.commit()
#     db.refresh(aluno)
#     return aluno

# # Listar alunos
# @app.get("/alunos")
# def listar_alunos(db: Session = Depends(get_db)):
#     return db.query(Aluno).all()


# # Atualizar aluno
# @app.put("/alunos/{aluno_id}")
# def atualizar_aluno(aluno_id: int, nome: str, email: str, db: Session = Depends(get_db)):
#     aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()

#     if not aluno:
#         raise HTTPException(status_code=404, detail="Aluno não encontrado")

#     aluno.nome = nome
#     aluno.email = email
#     db.commit()
#     db.refresh(aluno)
#     return aluno

# # Deletar aluno
# @app.delete("/alunos/{aluno_id}")
# def deletar_aluno(aluno_id: int, db: Session = Depends(get_db)):
#     aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()

#     if not aluno:
#         raise HTTPException(status_code=404, detail="Aluno não encontrado")

#     db.delete(aluno)
#     db.commit()
#     return {"message": f"Aluno com ID {aluno_id} deletado com sucesso"}


# # Criar curso
# @app.post("/cursos")
# def criar_curso(nome: str, descricao: str, db: Session = Depends(get_db)):
#     curso = Curso(nome=nome, descricao=descricao)
#     db.add(curso)
#     db.commit()
#     db.refresh(curso)
#     return curso

# # Listar cursos
# @app.get("/cursos")
# def listar_cursos(db: Session = Depends(get_db)):
#     return db.query(Curso).all()

# # Criar inscrição
# @app.post("/inscricoes")
# def criar_inscricao(aluno_id: int, curso_id: int, db: Session = Depends(get_db)):
#     aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()
#     curso = db.query(Curso).filter(Curso.id == curso_id).first()

#     if not aluno or not curso:
#         raise HTTPException(status_code=404, detail="Aluno ou Curso não encontrados")
    
#     inscricao = Inscricao(aluno_id=aluno_id, curso_id=curso_id)
#     db.add(inscricao)
#     db.commit()
#     db.refresh(inscricao)
#     return inscricao

# # Listar inscrições
# @app.get("/inscricoes")
# def listar_inscricoes(db: Session = Depends(get_db)):
#     return db.query(Inscricao).all()
