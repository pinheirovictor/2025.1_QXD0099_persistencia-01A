# Importa a função create_engine do SQLAlchemy, que é usada para criar uma conexão com o banco de dados
from sqlalchemy import create_engine

# Importa a função declarative_base, que serve como base para definir os modelos ORM
from sqlalchemy.ext.declarative import declarative_base

# Importa sessionmaker, uma fábrica para criar instâncias de sessão do banco de dados
from sqlalchemy.orm import sessionmaker

# Define a URL do banco de dados SQLite. Neste caso, o banco será armazenado em um arquivo local chamado "test.db"
DATABASE_URL = "sqlite:///./test.db"

# Cria o mecanismo de conexão (engine) com o banco de dados usando a URL definida
# O parâmetro connect_args={"check_same_thread": False} é necessário para que o SQLite possa ser usado em um ambiente multi-thread
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Cria uma fábrica de sessões configurada com:
# - autocommit=False: As transações não serão automaticamente confirmadas
# - autoflush=False: Não será feito um flush automático para sincronizar as alterações com o banco
# - bind=engine: Liga a sessão ao mecanismo de conexão criado anteriormente
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define a base para a criação de classes de modelo ORM
# Todos os modelos do SQLAlchemy herdarão dessa base
Base = declarative_base()

# Função que fornece uma sessão de banco de dados para cada requisição
# Essa função utiliza um gerador (yield) para garantir que a sessão seja aberta e fechada corretamente
def get_db():
    db = SessionLocal()  # Cria uma nova sessão do banco
    try:
        yield db  # Retorna a sessão para o código que requisitar
    finally:
        db.close()  # Fecha a sessão após o uso, garantindo que os recursos sejam liberados


