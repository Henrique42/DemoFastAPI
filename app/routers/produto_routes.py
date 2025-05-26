from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session  
  
import app.schemas.produto_schema as schemas
from app.crud.produto_crud import (  
    create_produto_crud,  
    delete_produto_crud,  
    get_produtos_crud,  
    get_produto_crud,  
    update_produto_crud,  
)
from app.database import get_db  
  
router = APIRouter()  
  
  
@router.post(  
    "/produto",  
    status_code=status.HTTP_201_CREATED,  
    response_model=schemas.ProdutoResponseModel,  
)  
def create_produto(  
    produto: schemas.ProdutoCreateModel, db: Session = Depends(get_db)  
) -> schemas.ProdutoResponseModel:  
    """  
    Criar um novo produto.  
    """  
    return create_produto_crud(payload=produto, db=db)  
  
  
@router.get(  
    "/produto/{produto_id}",  
    status_code=status.HTTP_200_OK,  
    response_model=schemas.ProdutoResponseModel,  
)  
def get_produto(  
    produto_id: str, db: Session = Depends(get_db)  
) -> schemas.ProdutoResponseModel:  
    """  
    Buscar produto pelo ID.  
    """  
    return get_produto_crud(produto_id=produto_id, db=db)  
  
  
@router.patch(  
    "/produto/{produto_id}",  
    status_code=status.HTTP_202_ACCEPTED,  
    response_model=schemas.ProdutoResponseModel,  
)  
def update_produto(  
    produto_id: str,  
    produto: schemas.ProdutoUpdateModel,  
    db: Session = Depends(get_db),  
) -> schemas.ProdutoResponseModel:  
    """  
    Atualizar produto pelo ID.  
    """  
    return update_produto_crud(produto_id=produto_id, payload=produto, db=db)  
  
  
@router.delete(  
    "/produto/{produto_id}",  
    status_code=status.HTTP_202_ACCEPTED,  
    response_model=schemas.ProdutoDeleteModel,  
)  
def delete_produto(  
    produto_id: str, db: Session = Depends(get_db)  
) -> schemas.ProdutoDeleteModel:  
    """  
    Deletar produto pelo ID.  
    """  
    return delete_produto_crud(produto_id=produto_id, db=db)  
  

# Paginação

@router.get(
    "/produto",
    status_code=status.HTTP_200_OK,
    response_model=schemas.ProdutoListResponseModel,
)
def get_produtos(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="Número de itens para pular"),
    limit: int = Query(10, gt=0, le=100, description="Número máximo de itens a serem retornados"),
) -> schemas.ProdutoListResponseModel:
    """
    Listar todos os produtos (com paginação).
    """
    return get_produtos_crud(db=db, skip=skip, limit=limit)