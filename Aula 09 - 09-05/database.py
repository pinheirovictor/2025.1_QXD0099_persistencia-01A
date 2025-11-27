# Importações necessárias do SQLAlchemy para manipulação do banco de dados
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base  # Importa a classe Base usada para declarar os modelos (tabelas)

# URL de conexão com o banco de dados SQLite
# O arquivo do banco será criado com o nome 'escola.db' no diretório atual
DATABASE_URL = "sqlite:///./escola.db"

# Cria o *engine*, que é o objeto responsável por se conectar ao banco
# O parâmetro `check_same_thread=False` é necessário no SQLite quando usamos o banco em contextos multithread (ex: FastAPI)
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Cria as tabelas no banco de dados com base nos modelos definidos que herdam de `Base`
# Caso as tabelas já existam, nada será sobrescrito
Base.metadata.create_all(bind=engine)

# Cria a *fábrica de sessões* que serão utilizadas para interagir com o banco
# autocommit=False → requer que o commit seja feito manualmente
# autoflush=False → evita envio automático das alterações ao banco
# bind=engine → associa a sessão ao banco criado
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Função que fornece uma sessão de banco para ser usada nos endpoints da API
# O `yield` permite usar essa função como uma dependência no FastAPI com gerenciamento automático
def get_db():
    db = SessionLocal()  # Cria uma nova sessão
    try:
        yield db  # Entrega a sessão para quem está chamando
    finally:
        db.close()  # Garante que a sessão será fechada após o uso


