from fastapi_crudrouter import SQLAlchemyCRUDRouter
from fastapi import Depends, Query
from sqlmodel import select, Session
from models.order_product import OrderProduct, OrderProductRead, OrderProductCreate
from core.database import get_session

router = SQLAlchemyCRUDRouter(
    schema=OrderProductRead,
    create_schema=OrderProductCreate,
    db_model=OrderProduct,
    db=get_session,
    prefix="/pedido_produtos"
)

@router.get("/paginado", response_model=list[OrderProductRead])
def get_order_products_paginated(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    session: Session = Depends(get_session)
):
    return session.exec(select(OrderProduct).offset(skip).limit(limit)).all()
