from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session  
  
import app.schemas.cliente_schema as schemas
from app.crud.cliente_crud import (  
    create_cliente_crud,  
    delete_cliente_crud,  
    get_clientes_crud,  
    get_cliente_crud,  
    update_cliente_crud,  
)
from app.database import get_db  
  
router = APIRouter()  
  
  
@router.post(  
    "/cliente",  
    status_code=status.HTTP_201_CREATED,  
    response_model=schemas.ClienteResponseModel,  
)  
def create_cliente(  
    cliente: schemas.ClienteCreateModel, db: Session = Depends(get_db)  
) -> schemas.ClienteResponseModel:  
    """  
    Criar um novo cliente.  
    """  
    return create_cliente_crud(payload=cliente, db=db)  
  
  
@router.get(  
    "/cliente/{cliente_id}",  
    status_code=status.HTTP_200_OK,  
    response_model=schemas.ClienteResponseModel,  
)  
def get_cliente(  
    cliente_id: str, db: Session = Depends(get_db)  
) -> schemas.ClienteResponseModel:  
    """  
    Buscar cliente pelo ID.  
    """  
    return get_cliente_crud(cliente_id=cliente_id, db=db)  
  
  
@router.patch(  
    "/cliente/{cliente_id}",  
    status_code=status.HTTP_202_ACCEPTED,  
    response_model=schemas.ClienteResponseModel,  
)  
def update_cliente(  
    cliente_id: str,  
    cliente: schemas.ClienteUpdateModel,  
    db: Session = Depends(get_db),  
) -> schemas.ClienteResponseModel:  
    """  
    Atualizar cliente pelo ID.  
    """  
    return update_cliente_crud(cliente_id=cliente_id, payload=cliente, db=db)  
  
  
@router.delete(  
    "/cliente/{cliente_id}",  
    status_code=status.HTTP_202_ACCEPTED,  
    response_model=schemas.ClienteDeleteModel,  
)  
def delete_cliente(  
    cliente_id: str, db: Session = Depends(get_db)  
) -> schemas.ClienteDeleteModel:  
    """  
    Deletar cliente pelo ID.  
    """  
    return delete_cliente_crud(cliente_id=cliente_id, db=db)  
  

# Paginação

@router.get(
    "/cliente",
    status_code=status.HTTP_200_OK,
    response_model=schemas.ClienteListResponseModel,
)
def get_clientes(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="Número de itens para pular"),
    limit: int = Query(10, gt=0, le=100, description="Número máximo de itens a serem retornados"),
) -> schemas.ClienteListResponseModel:
    """
    Listar todos os clientes (com paginação).
    """
    return get_clientes_crud(db=db, skip=skip, limit=limit)