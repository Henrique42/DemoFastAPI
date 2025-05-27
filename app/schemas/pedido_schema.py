from datetime import date, datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class Status(Enum):
    Success = "Successo"
    Error = "Erro"


class StatusPedidoEnum(str, Enum):
    PENDENTE = "pendente"
    PROCESSANDO = "processando"
    ENVIADO = "enviado"
    ENTREGUE = "entregue"
    CANCELADO = "cancelado"


class PedidoProdutoBaseModel(BaseModel):
    produto_id: int = Field(..., example=1, description="ID do produto")
    quantidade: int = Field(..., gt=0, example=2, description="Quantidade do produto no pedido")

    model_config = ConfigDict(from_attributes=True)


class PedidoProdutoCreateModel(PedidoProdutoBaseModel):
    pass


class PedidoProdutoModel(PedidoProdutoBaseModel):
    id: int

    model_config = ConfigDict(from_attributes=True)


class PedidoBaseModel(BaseModel):
    cliente_id: int = Field(..., example=1, description="ID do cliente que fez o pedido")
    d_pedido: Optional[datetime] = Field(None, example="2025-05-26T14:30:00Z", description="Data e hora do pedido")
    status: Optional[StatusPedidoEnum] = Field(StatusPedidoEnum.PENDENTE, description="Status do pedido")
    periodo_inicio: Optional[date] = Field(None, example="2025-05-01", description="Início do período do pedido")
    periodo_fim: Optional[date] = Field(None, example="2025-05-31", description="Fim do período do pedido")
    produtos: Optional[List[PedidoProdutoCreateModel]] = []

    model_config = ConfigDict(from_attributes=True)


class PedidoCreateModel(PedidoBaseModel):
    pass


class PedidoUpdateModel(BaseModel):
    status: Optional[StatusPedidoEnum] = Field(None, description="Atualização do status do pedido")
    periodo_inicio: Optional[date] = Field(None, description="Atualização do início do período")
    periodo_fim: Optional[date] = Field(None, description="Atualização do fim do período")
    produtos: Optional[List[PedidoProdutoCreateModel]] = None  # Permite atualizar produtos se necessário

    model_config = ConfigDict(from_attributes=True)


class PedidoModel(PedidoBaseModel):
    id: int

    model_config = ConfigDict(from_attributes=True)


class PedidoResponseModel(BaseModel):
    status: Status = Status.Success
    message: str
    data: PedidoModel

    model_config = ConfigDict(from_attributes=True)


class PedidoListResponseModel(BaseModel):
    status: Status = Status.Success
    message: str
    data: List[PedidoModel]

    model_config = ConfigDict(from_attributes=True)


class PedidoDeleteModel(BaseModel):
    id: int
    status: Status = Status.Success
    message: str

    model_config = ConfigDict(from_attributes=True)
