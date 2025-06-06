# Importa o SQLAlchemyCRUDRouter da biblioteca fastapi_crudrouter, 
# que fornece um roteador pronto para operações CRUD (Create, Read, Update, Delete)
from fastapi_crudrouter import SQLAlchemyCRUDRouter

# Importa o modelo User definido na aplicação
from models import User

# Importa a função get_db, que é usada para gerenciar as sessões de banco de dados
from database import get_db

# Importa a classe BaseModel da biblioteca Pydantic, que será usada para criar esquemas de validação
from pydantic import BaseModel

# Definição do esquema Pydantic para validação de dados do modelo User
class UserSchema(BaseModel):
    id: int  # Campo obrigatório representando o ID do usuário
    name: str  # Campo obrigatório representando o nome do usuário
    email: str  # Campo obrigatório representando o email do usuário

    # Configuração adicional para o esquema Pydantic
    class Config:
        orm_mode = True  # Habilita o suporte para interagir diretamente com objetos ORM

# Configuração do roteador CRUD utilizando o SQLAlchemyCRUDRouter
router = SQLAlchemyCRUDRouter(
    schema=UserSchema,  # Especifica o esquema Pydantic para validação de dados
    db_model=User,      # Indica o modelo SQLAlchemy correspondente ao esquema
    db=get_db           # Define a função que retorna a sessão do banco de dados
)

