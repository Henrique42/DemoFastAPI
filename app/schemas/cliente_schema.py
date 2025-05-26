from enum import Enum  
from typing import List, Optional
  
from pydantic import BaseModel, ConfigDict, EmailStr, Field  
  
class Status(Enum):  
    Success = "Successo"  
    Error = "Erro"  
  
  
class ClienteBaseModel(BaseModel):  
    
    nome: Optional[str] = Field(  
        default=None,  
        json_schema_extra={  
            "example": "João Cliente",  
            "description": "Nome do cliente",  
        },  
    )
    email: Optional[EmailStr] = Field(  
        default=None,  
        json_schema_extra={  
            "example": "exemplo@email.com",  
            "description": "E-mail do cliente",  
        },  
    )
    cpf: Optional[str] = Field(  
        default=None,  
        json_schema_extra={  
            "example": "000.000.000-00",  
            "description": "CPF do cliente",  
        },  
    )
    model_config = ConfigDict(from_attributes=True)  
  
  
class ClienteCreateModel(ClienteBaseModel):
    pass
  
  
class ClienteUpdateModel(ClienteBaseModel):  
    ativo: bool 
    model_config = ConfigDict(from_attributes=True)  
  
  
class ClienteModel(ClienteBaseModel):  
    id: int
    ativo: bool
    model_config = ConfigDict(from_attributes=True)  
  
  
class ClienteResponseModel(BaseModel):  
    status: Status = Status.Success  
    message: str  
    data: ClienteModel  
  
  
class ClienteListResponseModel(BaseModel):  
    status: Status = Status.Success  
    message: str  
    data: List[ClienteModel]  
  
  
class ClienteDeleteModel(BaseModel):  
    id: int  
    status: Status = Status.Success  
    message: str  