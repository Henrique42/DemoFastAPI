from fastapi import Depends, HTTPException, status  
from sqlalchemy.exc import IntegrityError, SQLAlchemyError  
from sqlalchemy.orm import Session  
  
import app.models as models  
import app.schemas.cliente_schema as schemas
from app.database import get_db
  
  
def create_cliente_crud( payload: schemas.ClienteCreateModel, db: Session = Depends(get_db)):  
    try:  
        new_cliente = models.ClienteOrm(**payload.model_dump())  
        db.add(new_cliente)  
        db.commit()  
        db.refresh(new_cliente)  
  
        cliente_data = schemas.ClienteModel.model_validate(new_cliente)  
  
        return schemas.ClienteResponseModel(  
            status=schemas.Status.Success,  
            message="Cliente criado com sucesso.",  
            data=cliente_data,  
        )  
    except IntegrityError:  
        db.rollback()  
        raise HTTPException(  
            status_code=status.HTTP_409_CONFLICT,  
            detail="O cliente que você está tentando adicionar já existe.",  
        )  
    except Exception as e:  
        db.rollback()  
        raise HTTPException(  
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,  
            detail=f"Um erro ocorreu ao tentar adicionar o cliente: {str(e)}",  
        )  
  
  
def get_cliente_crud(cliente_id: str, db: Session = Depends(get_db)):  
    cliente_data = (  
        db.query(models.ClienteOrm)  
        .filter(models.ClienteOrm.id == cliente_id)  
        .first()  
    )  
  
    if not cliente_data:  
        raise HTTPException(  
            status_code=status.HTTP_404_NOT_FOUND,  
            detail="Cliente não encontrado.",  
        )  
  
    try:  
        return schemas.ClienteResponseModel(  
            status=schemas.Status.Success,  
            message="Cliente retornado com sucesso.",  
            data=schemas.ClienteModel.model_validate(cliente_data),  
        )  
    except SQLAlchemyError as e:  
        raise HTTPException(  
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,  
            detail="Um erro ocorreu ao tentar retornar o cliente.",  
        ) from e  
  
  
def update_cliente_crud( cliente_id: str, payload: schemas.ClienteUpdateModel, db: Session):  
    cliente_query = db.query(models.ClienteOrm).filter(  
        models.ClienteOrm.id == cliente_id  
    )  
    db_cliente = cliente_query.first()  
  
    if not db_cliente:  
        raise HTTPException(  
            status_code=status.HTTP_404_NOT_FOUND, detail="Cliente não encontrado."  
        )  
  
    try:  
        # Prepare update data from the payload, only including fields that are set  
        update_data = payload.model_dump(exclude_unset=True)  
        if update_data:  
            cliente_query.update(update_data, synchronize_session="evaluate")  
            db.commit()  
            db.refresh(db_cliente)  
  
            # Convert the updated ORM model back to a Pydantic model  
            return schemas.ClienteResponseModel(  
                status=schemas.Status.Success,  
                message="Cliente atualizado com successo.",  
                data=schemas.ClienteModel.model_validate(db_cliente),  
            )  
        else:  
            raise HTTPException(  
                status_code=status.HTTP_400_BAD_REQUEST,  
                detail="Campo(s) inválido(s).",  
            )  
    except IntegrityError as e:  
        db.rollback()  
        raise HTTPException(  
            status_code=status.HTTP_409_CONFLICT,  
            detail="O cliente que você está tentando adicionar já existe.",  
        ) from e  
    except SQLAlchemyError as e:  
        db.rollback()  
        raise HTTPException(  
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,  
            detail=f"Um erro ocorreu ao tentar atualizar o cliente: {str(e)}",  
        ) from e  
  
  
def delete_cliente_crud(cliente_id: str, db: Session = Depends(get_db)):  
    try:  
        cliente_query = db.query(models.ClienteOrm).filter(  
            models.ClienteOrm.id == cliente_id  
        )  
        cliente_ = cliente_query.first()  
        if not cliente_:  
            raise HTTPException(  
                status_code=status.HTTP_404_NOT_FOUND,  
                detail=f"Não foi encontrado nenhum cliente com o ID: {cliente_id}",  
            )  
        cliente_query.delete(synchronize_session=False)  
        db.commit()  
        return schemas.ClienteDeleteModel(  
            id=cliente_id,  
            status=schemas.Status.Success,  
            message="Cliente removido com successo.",  
        )  
    except Exception as e:  
        db.rollback()  
        raise HTTPException(  
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,  
            detail="Um erro ocorreu ao tentar remover o cliente.",  
        ) from e  
  
  
def get_clientes_crud( db: Session = Depends(get_db), limit: int = 10, skip: int = 0, page: int = 1, search: str = ""):  
  
    clientes = db.query(models.ClienteOrm).limit(limit).offset(skip).all()  
    return schemas.ClienteListResponseModel(  
        status=schemas.Status.Success,  
        message="Lista com todos os clientes obtida com sucesso.",  
        data=[  
            schemas.ClienteModel.model_validate(cliente_) for cliente_ in clientes  
        ],  
    )
