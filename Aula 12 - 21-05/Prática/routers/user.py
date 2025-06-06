from fastapi_crudrouter import SQLAlchemyCRUDRouter
from fastapi import Depends, Query
from sqlmodel import select, Session, func
from models.user import User, UserRead, UserCreate
from core.database import get_session
from models.user import User
from models.profile import Profile
from typing import List, Dict, Any


router = SQLAlchemyCRUDRouter(
    schema=UserRead,
    create_schema=UserCreate,
    db_model=User,
    db=get_session,
    prefix="/usuarios"
)

# --- SOBRESCRITANDO A ROTA GET ALL PADRÃO DO CRUD ROUTER ---
# A rota GET / (que seria /usuarios/) é a que você quer que seja paginada.
# O decorator `@router.get("/")` irá sobrescrever a implementação padrão do CRUD Router para GET ALL.
@router.get("/", response_model=Dict[str, Any], summary="Listar todos os usuários paginados")
def get_users_paginated_custom( # Renomeei para evitar conflito com o nome anterior se estivesse no main.py
    page: int = Query(1, ge=1, description="Número da página, padrão 1, mínimo 1"),
    page_size: int = Query(10, ge=1, le=100, description="Tamanho da página, entre 1 e 100"),
    session: Session = Depends(get_session)
):
    """
    Lista todos os usuários com paginação e metadados.
    Esta rota sobrescreve a listagem padrão do CRUD Router.
    """
    total_records = session.exec(select(func.count(User.id))).one()

    # Cálculos para paginação
    offset = (page - 1) * page_size if page_size > 0 else 0
    total_pages = (total_records + page_size - 1) // page_size if page_size > 0 else (1 if total_records > 0 else 0)

    # Consulta os usuários com offset e limit
    query = select(User).offset(offset).limit(page_size)
    results = session.exec(query).all()

    # Formata os resultados para o schema de leitura
    formatted_results = [UserRead.from_orm(user) for user in results]

    return {
        "data": formatted_results,
        "pagination": {
            "total_records": total_records,
            "total_pages": total_pages,
            "current_page": page,
            "page_size": page_size
        }
    }
    
    
@router.get("/usuarios-perfis/{item_id}")
def usuario_perfil_por_id(item_id: int, session: Session = Depends(get_session)):
    statement = (
        select(User, Profile)
        .join(Profile, Profile.user_id == User.id, isouter=True)
        .where(User.id == item_id)
    )
    result = session.exec(statement).first()
    if not result:
        return {"error": "Usuário não encontrado"}
    user, profile = result
    return {
        "usuario_id": user.id,
        "nome": user.nome,
        "email": user.email,
        "perfil": {
            "endereco": profile.endereco,
            "telefone": profile.telefone
        } if profile else None
    }