from pydantic import BaseModel, Field, EmailStr, GetCoreSchemaHandler
from pydantic_core import core_schema
from typing import List, Optional
from bson import ObjectId

# Tipo customizado para campos de ID do MongoDB (ObjectId)
class PyObjectId(ObjectId):
    # Integra o tipo ObjectId ao sistema de validação do Pydantic v2+
    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type, handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        # Diz ao Pydantic para usar a função validate abaixo, sem infos extras
        return core_schema.no_info_plain_validator_function(cls.validate)

    @classmethod
    def validate(cls, v):
        # Verifica se o valor recebido é um ObjectId válido
        if not ObjectId.is_valid(v):
            raise ValueError("ID inválido")
        return ObjectId(v)  # Retorna um ObjectId válido

    @classmethod
    def __get_pydantic_json_schema__(cls, schema, handler):
        # Garante que o OpenAPI/Swagger veja esse campo como string
        return {'type': 'string'}

# -------- MODELOS PROFESSOR --------

# Base do professor (campos usados em criação e resposta)
class ProfessorBase(BaseModel):
    nome: str
    especialidade: str
    email: EmailStr  # Valida se é um e-mail real

# Modelo para criação (entrada no POST)
class ProfessorCreate(ProfessorBase):
    pass

# Modelo para saída (resposta nas rotas), inclui id
class ProfessorOut(ProfessorBase):
    id: Optional[str] = Field(alias="_id")  # Recebe o _id do MongoDB como string

    class Config:
        json_encoders = {ObjectId: str}      # Serializa ObjectId como string no JSON
        populate_by_name = True              # Permite que o alias (_id) seja populado por id

# -------- MODELOS CURSO --------

class CursoBase(BaseModel):
    nome: str
    descricao: str
    carga_horaria: int
    professor_id: str  # Referência ao Professor (id em formato string)
    alunos: List[str] = []
    turmas: List[str] = []
    departamento_id: str 

class CursoCreate(CursoBase):
    pass

class CursoOut(CursoBase):
    id: Optional[str] = Field(alias="_id")

    class Config:
        json_encoders = {ObjectId: str}
        populate_by_name = True

# -------- MODELOS ALUNO --------

class AlunoBase(BaseModel):
    nome: str
    email: EmailStr
    idade: int
    curso_id: str

class AlunoCreate(AlunoBase):
    pass

class AlunoOut(AlunoBase):
    id: Optional[str] = Field(alias="_id")

    class Config:
        json_encoders = {ObjectId: str}
        populate_by_name = True

# -------- MODELOS TURMA --------

class TurmaBase(BaseModel):
    nome: str
    curso_id: str           # Curso associado (id em formato string)
    # alunos: List[str] = []  # Lista de alunos (cada um representado por id em string)

class TurmaCreate(TurmaBase):
    pass

class TurmaOut(TurmaBase):
    id: Optional[str] = Field(alias="_id")

    class Config:
        json_encoders = {ObjectId: str}
        populate_by_name = True

# -------- MODELOS DEPARTAMENTO --------

class DepartamentoBase(BaseModel):
    nome: str
    chefe_id: str           # Professor chefe (id em string)
    cursos: List[str] = []  # Cursos do departamento (ids em string)

class DepartamentoCreate(DepartamentoBase):
    pass

class DepartamentoOut(DepartamentoBase):
    id: Optional[str] = Field(alias="_id")

    class Config:
        json_encoders = {ObjectId: str}
        populate_by_name = True

# -------- MODELOS MATRÍCULA (Aluno-Curso) --------

class MatriculaBase(BaseModel):
    aluno_id: str  # id do aluno (string)
    turma_id: str  # id do curso (string)

class MatriculaCreate(MatriculaBase):
    pass

class MatriculaOut(MatriculaBase):
    id: Optional[str] = Field(alias="_id")

    class Config:
        json_encoders = {ObjectId: str}
        populate_by_name = True

# -------- MODELOS MATRÍCULA EMBEDDED (Aluno e Curso completos) --------

class MatriculaEmbeddedOut(BaseModel):
    id: Optional[str] = Field(alias="_id")
    aluno: Optional[AlunoOut]  # Usando modelo AlunoOut completo
    turma: Optional[TurmaOut]  # Usando modelo CursoOut completo

    class Config:
        json_encoders = {ObjectId: str}
        populate_by_name = True
