# Importa recursos essenciais do SQLAlchemy:
# - relationship: para definir relacionamentos entre tabelas (1:N, N:1 etc.)
# - declarative_base: para criar uma base comum usada pelas classes (modelos)
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey

# Cria a base para os modelos. Todas as classes de modelo devem herdar dessa base.
Base = declarative_base()

# Define a tabela 'alunos' no banco de dados
class Aluno(Base):
    __tablename__ = 'alunos'  # Nome da tabela no banco

    id = Column(Integer, primary_key=True)  # Chave primária (PK)
    nome = Column(String, nullable=False)  # Campo obrigatório
    email = Column(String, unique=True, nullable=False)  # Campo obrigatório e único (não pode repetir)

    # Relacionamento 1:N → Um aluno pode ter várias inscrições
    # back_populates conecta os dois lados do relacionamento
    inscricoes = relationship('Inscricao', back_populates='aluno')

# Define a tabela 'cursos'
class Curso(Base):
    __tablename__ = 'cursos'

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    descricao = Column(String)

    # Relacionamento 1:N → Um curso pode ter várias inscrições
    inscricoes = relationship('Inscricao', back_populates='curso')

# Define a tabela 'inscricoes', que representa o relacionamento N:N entre alunos e cursos
class Inscricao(Base):
    __tablename__ = 'inscricoes'

    id = Column(Integer, primary_key=True)
    
    # Chave estrangeira (FK) que referencia o aluno inscrito
    aluno_id = Column(Integer, ForeignKey('alunos.id'))

    # Chave estrangeira (FK) que referencia o curso inscrito
    curso_id = Column(Integer, ForeignKey('cursos.id'))

    # Relacionamento N:1 com Aluno
    aluno = relationship('Aluno', back_populates='inscricoes')

    # Relacionamento N:1 com Curso
    curso = relationship('Curso', back_populates='inscricoes')


        
        
        
