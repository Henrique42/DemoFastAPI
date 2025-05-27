from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session  
  
import app.schemas.pedido_schema as schemas
from app.crud.pedido_crud import (  
    create_pedido_crud,  
    delete_pedido_crud,  
    get_pedidos_crud,  
    get_pedido_crud,  
    update_pedido_crud,  
)
from app.database import get_db  
  
router = APIRouter()  
  
  
@router.post(  
    "/pedido",  
    status_code=status.HTTP_201_CREATED,  
    response_model=schemas.PedidoResponseModel,  
)  
def create_pedido(  
    pedido: schemas.PedidoCreateModel, db: Session = Depends(get_db)  
) -> schemas.PedidoResponseModel:  
    """  
    Criar um novo pedido.  
    """  
    return create_pedido_crud(payload=pedido, db=db)  
  
  
@router.get(  
    "/pedido/{pedido_id}",  
    status_code=status.HTTP_200_OK,  
    response_model=schemas.PedidoResponseModel,  
)  
def get_pedido(  
    pedido_id: str, db: Session = Depends(get_db)  
) -> schemas.PedidoResponseModel:  
    """  
    Buscar pedido pelo ID.  
    """  
    return get_pedido_crud(pedido_id=pedido_id, db=db)  
  
  
@router.patch(  
    "/pedido/{pedido_id}",  
    status_code=status.HTTP_202_ACCEPTED,  
    response_model=schemas.PedidoResponseModel,  
)  
def update_pedido(  
    pedido_id: str,  
    pedido: schemas.PedidoUpdateModel,  
    db: Session = Depends(get_db),  
) -> schemas.PedidoResponseModel:  
    """  
    Atualizar pedido pelo ID.  
    """  
    return update_pedido_crud(pedido_id=pedido_id, payload=pedido, db=db)  
  
  
@router.delete(  
    "/pedido/{pedido_id}",  
    status_code=status.HTTP_202_ACCEPTED,  
    response_model=schemas.PedidoDeleteModel,  
)  
def delete_pedido(  
    pedido_id: str, db: Session = Depends(get_db)  
) -> schemas.PedidoDeleteModel:  
    """  
    Deletar pedido pelo ID.  
    """  
    return delete_pedido_crud(pedido_id=pedido_id, db=db)  
  

# Paginação

@router.get(
    "/pedido",
    status_code=status.HTTP_200_OK,
    response_model=schemas.PedidoListResponseModel,
)
def get_pedidos(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="Número de itens para pular"),
    limit: int = Query(10, gt=0, le=100, description="Número máximo de itens a serem retornados"),
) -> schemas.PedidoListResponseModel:
    """
    Listar todos os pedidos (com paginação).
    """
    return get_pedidos_crud(db=db, skip=skip, limit=limit)