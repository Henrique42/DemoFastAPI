from fastapi import Depends, HTTPException, status  
from sqlalchemy.exc import IntegrityError, SQLAlchemyError  
from sqlalchemy.orm import Session  
  
import app.models as models  
import app.schemas.produto_schema as schemas
from app.database import get_db
  
  
def create_produto_crud(payload: schemas.ProdutoCreateModel, db: Session = Depends(get_db)):
    try:
        data = payload.model_dump()
        
        # Remove imagens do dict, para tratar separadamente
        imagens_data = data.pop("imagens", [])
        
        # Cria o ProdutoOrm com os dados sem imagens
        new_produto = models.ProdutoOrm(**data)
        
        # Cria instâncias ORM para as imagens e associa
        new_produto.imagens = [models.ProdutoImagemOrm(**img) for img in imagens_data]
        
        db.add(new_produto)
        db.commit()
        db.refresh(new_produto)
        
        produto_data = schemas.ProdutoModel.model_validate(new_produto)
        return schemas.ProdutoResponseModel(
            status=schemas.Status.Success,
            message="Produto criado com sucesso.",
            data=produto_data,
        )
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"O produto que você está tentando adicionar já existe.",
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Um erro ocorreu ao tentar adicionar o produto: {str(e)}",
        )

  
  
def get_produto_crud(produto_id: str, db: Session = Depends(get_db)):  
    produto_data = (  
        db.query(models.ProdutoOrm)  
        .filter(models.ProdutoOrm.id == produto_id)  
        .first()  
    )  
  
    if not produto_data:  
        raise HTTPException(  
            status_code=status.HTTP_404_NOT_FOUND,  
            detail="Produto não encontrado.",  
        )  
  
    try:  
        return schemas.ProdutoResponseModel(  
            status=schemas.Status.Success,  
            message="Produto retornado com sucesso.",  
            data=schemas.ProdutoModel.model_validate(produto_data),  
        )  
    except SQLAlchemyError as e:  
        raise HTTPException(  
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,  
            detail="Um erro ocorreu ao tentar retornar o produto.",  
        ) from e  
  
  
def update_produto_crud(produto_id: int, payload: schemas.ProdutoUpdateModel, db: Session):
    produto_query = db.query(models.ProdutoOrm).filter(models.ProdutoOrm.id == produto_id)
    db_produto = produto_query.first()

    if not db_produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado."
        )

    try:
        update_data = payload.model_dump(exclude_unset=True)

        # Se tiver imagens no update, vamos tratar separado
        imagens_data = update_data.pop("imagens", None)

        if update_data:
            produto_query.update(update_data, synchronize_session="evaluate")
            db.commit()
            db.refresh(db_produto)

        if imagens_data is not None:
            # Apaga as imagens antigas (porque o cascade "delete-orphan" está configurado)
            db_produto.imagens.clear()
            db.flush()  # Garante que a remoção é feita antes da inserção
            
            # Cria e adiciona as novas imagens
            novas_imagens = [models.ProdutoImagemOrm(**img) for img in imagens_data]
            db_produto.imagens.extend(novas_imagens)

            db.commit()
            db.refresh(db_produto)

        return schemas.ProdutoResponseModel(
            status=schemas.Status.Success,
            message="Produto atualizado com sucesso.",
            data=schemas.ProdutoModel.model_validate(db_produto),
        )

    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="O produto que você está tentando atualizar já existe.",
        ) from e
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Um erro ocorreu ao tentar atualizar o produto: {str(e)}",
        ) from e
  
def delete_produto_crud(produto_id: int, db: Session = Depends(get_db)):
    try:
        produto_ = db.query(models.ProdutoOrm).filter(models.ProdutoOrm.id == produto_id).first()
        if not produto_:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Não foi encontrado nenhum produto com o ID: {produto_id}",
            )
        db.delete(produto_)  # Deleta o objeto ORM, cascata funciona aqui
        db.commit()
        return schemas.ProdutoDeleteModel(
            id=produto_id,
            status=schemas.Status.Success,
            message="Produto removido com sucesso.",
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Um erro ocorreu ao tentar remover o produto.",
        ) from e  
  
def get_produtos_crud( db: Session = Depends(get_db), limit: int = 10, skip: int = 0, page: int = 1, search: str = ""):  
  
    produtos = db.query(models.ProdutoOrm).limit(limit).offset(skip).all()  
    return schemas.ProdutoListResponseModel(  
        status=schemas.Status.Success,  
        message="Lista com todos os produtos obtida com sucesso.",  
        data=[  
            schemas.ProdutoModel.model_validate(produto_) for produto_ in produtos  
        ],  
    )
