from fastapi_crudrouter import SQLAlchemyCRUDRouter
from fastapi import Depends, Query
from sqlmodel import select, Session
from models.order import Order, OrderRead, OrderCreate
from core.database import get_session

router = SQLAlchemyCRUDRouter(
    schema=OrderRead,
    create_schema=OrderCreate,
    db_model=Order,
    db=get_session,
    prefix="/pedidos"
)

@router.get("/paginado", response_model=list[OrderRead])
def get_orders_paginated(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    session: Session = Depends(get_session)
):
    return session.exec(select(Order).offset(skip).limit(limit)).all()
