from fastapi_crudrouter import SQLAlchemyCRUDRouter
from fastapi import Depends, Query
from sqlmodel import select, Session
from models.product import Product, ProductRead, ProductCreate
from core.database import get_session

router = SQLAlchemyCRUDRouter(
    schema=ProductRead,
    create_schema=ProductCreate,
    db_model=Product,
    db=get_session,
    prefix="/produtos"
)

@router.get("/paginado", response_model=list[ProductRead])
def get_products_paginated(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    session: Session = Depends(get_session)
):
    return session.exec(select(Product).offset(skip).limit(limit)).all()
