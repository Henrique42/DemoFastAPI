from datetime import date
from enum import Enum  
from typing import List, Optional
  
from pydantic import BaseModel, ConfigDict, constr, EmailStr, Field  
  
class Status(Enum):  
    Success = "Successo"  
    Error = "Erro"  
  
class ProdutoImagemModel(BaseModel):
    url: str
    model_config = ConfigDict(from_attributes=True)  

class ProdutoBaseModel(BaseModel):  
    nome: Optional[str] = Field(  
        default=None,
        max_length=255,
        example="Arroz Integral",
        description="Nome do produto"
    )
    descricao: Optional[str] = Field(
        default=None,
        max_length=255,
        example="Arroz Integral Dona Maria (1kg)",
        description="Descrição do produto"
    )
    preco: Optional[float] = Field(
        default=None,
        example=9.99,
        description="Preço do produto",
    )
    cod_barras: Optional[str] = Field(
        default=None,
        max_length=13,
        example="7891234567895",
        description="Código de barras do produto",
    )
    secao: Optional[str] = Field(
        default=None,
        max_length=50,
        example="Alimentos",
        description="Seção onde o produto está localizado",
    )
    estoque: Optional[int] = Field(
        default=0,
        example=50,
        description="Quantidade disponível em estoque",
    )
    data_validade: Optional[date] = Field(
        default=None,
        example="2025-12-31",
        description="Data de validade do produto",
    )
    imagens: Optional[List[ProdutoImagemModel]] = []
    model_config = ConfigDict(from_attributes=True)  
  
  
class ProdutoCreateModel(ProdutoBaseModel):
    pass
  
  
class ProdutoUpdateModel(ProdutoBaseModel):
    model_config = ConfigDict(from_attributes=True)  
  
  
class ProdutoModel(ProdutoBaseModel):  
    id: int
    model_config = ConfigDict(from_attributes=True)  
  
  
class ProdutoResponseModel(BaseModel):  
    status: Status = Status.Success  
    message: str  
    data: ProdutoModel  
  
  
class ProdutoListResponseModel(BaseModel):  
    status: Status = Status.Success  
    message: str  
    data: List[ProdutoModel]  
  
  
class ProdutoDeleteModel(BaseModel):  
    id: int  
    status: Status = Status.Success  
    message: str  