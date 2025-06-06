from fastapi_crudrouter import SQLAlchemyCRUDRouter
from fastapi import Depends, Query
from sqlmodel import select, Session
from models.profile import Profile, ProfileRead, ProfileCreate
from core.database import get_session

router = SQLAlchemyCRUDRouter(
    schema=ProfileRead,
    create_schema=ProfileCreate,
    db_model=Profile,
    db=get_session,
    prefix="/perfis"
)

@router.get("/paginado", response_model=list[ProfileRead])
def get_profiles_paginated(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    session: Session = Depends(get_session)
):
    return session.exec(select(Profile).offset(skip).limit(limit)).all()
