from fastapi import Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

import app.models as models
import app.schemas.pedido_schema as schemas
from app.database import get_db


def create_pedido_crud(payload: schemas.PedidoCreateModel, db: Session = Depends(get_db)):
    try:
        data = payload.model_dump()

        produtos_data = data.pop("produtos", [])

        new_pedido = models.PedidoOrm(**data)

        # Cria os objetos PedidoProdutoOrm e associa ao pedido
        new_pedido.produtos = [
            models.PedidoProdutoOrm(
                produto_id=produto["produto_id"],
                quantidade=produto["quantidade"]
            )
            for produto in produtos_data
        ]

        db.add(new_pedido)
        db.commit()
        db.refresh(new_pedido)

        pedido_data = schemas.PedidoModel.model_validate(new_pedido)
        return schemas.PedidoResponseModel(
            status=schemas.Status.Success,
            message="Pedido criado com sucesso.",
            data=pedido_data,
        )
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Pedido já existe ou dados inválidos.",
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar pedido: {str(e)}",
        )


def get_pedido_crud(pedido_id: int, db: Session = Depends(get_db)):
    pedido = db.query(models.PedidoOrm).filter(models.PedidoOrm.id == pedido_id).first()

    if not pedido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pedido não encontrado.",
        )

    try:
        return schemas.PedidoResponseModel(
            status=schemas.Status.Success,
            message="Pedido retornado com sucesso.",
            data=schemas.PedidoModel.model_validate(pedido),
        )
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao retornar pedido.",
        ) from e


def update_pedido_crud(pedido_id: int, payload: schemas.PedidoUpdateModel, db: Session):
    pedido_query = db.query(models.PedidoOrm).filter(models.PedidoOrm.id == pedido_id)
    db_pedido = pedido_query.first()

    if not db_pedido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pedido não encontrado.",
        )

    try:
        update_data = payload.model_dump(exclude_unset=True)

        produtos_data = update_data.pop("produtos", None)

        if update_data:
            pedido_query.update(update_data, synchronize_session="evaluate")
            db.commit()
            db.refresh(db_pedido)

        if produtos_data is not None:
            # Limpa os produtos antigos
            db_pedido.produtos.clear()
            db.flush()

            # Adiciona novos produtos
            novos_produtos = [
                models.PedidoProdutoOrm(
                    produto_id=p["produto_id"],
                    quantidade=p["quantidade"]
                )
                for p in produtos_data
            ]
            db_pedido.produtos.extend(novos_produtos)

            db.commit()
            db.refresh(db_pedido)

        return schemas.PedidoResponseModel(
            status=schemas.Status.Success,
            message="Pedido atualizado com sucesso.",
            data=schemas.PedidoModel.model_validate(db_pedido),
        )

    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Pedido com dados duplicados ou inválidos.",
        ) from e
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar pedido: {str(e)}",
        ) from e


def delete_pedido_crud(pedido_id: int, db: Session = Depends(get_db)):
    try:
        pedido = db.query(models.PedidoOrm).filter(models.PedidoOrm.id == pedido_id).first()
        if not pedido:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Pedido com ID {pedido_id} não encontrado.",
            )
        db.delete(pedido)
        db.commit()
        return schemas.PedidoDeleteModel(
            id=pedido_id,
            status=schemas.Status.Success,
            message="Pedido removido com sucesso.",
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao tentar remover o pedido.",
        ) from e


def get_pedidos_crud(db: Session = Depends(get_db), limit: int = 10, skip: int = 0):
    pedidos = db.query(models.PedidoOrm).limit(limit).offset(skip).all()
    return schemas.PedidoListResponseModel(
        status=schemas.Status.Success,
        message="Lista de pedidos obtida com sucesso.",
        data=[schemas.PedidoModel.model_validate(p) for p in pedidos],
    )
