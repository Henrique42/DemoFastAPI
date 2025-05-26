from typing import Dict
import fastapi
import uvicorn

# Importa utilitário para injeção de dependência e tipos de sessão do SQLAlchemy
from fastapi import Depends
from sqlalchemy.orm import Session

# Importa o controller de clientes e função para obter o banco
from app.controllers.cliente import ClientesController
from app.database import get_db

# Cria a aplicação FastAPI
app = fastapi.FastAPI()

# Rota raiz
@app.get("/")
def root():
    return {"Mensagem": "Boas-vindas!"}

# Rota de verificação de status
@app.get("/status")
def get_server_health():
    return {"status": "Servidor em funcionamento!"}

# Rota para adicionar cliente; recebe dados do corpo e uma sessão de banco
@app.post("/clientes/")
def add_cliente_api(body: Dict, db: Session = Depends(get_db)):
    return ClientesController(db).add_cliente(body)

# Rota para listar todos os clientes
@app.get("/clientes/")
def get_cliente_api(db: Session = Depends(get_db)):
    return ClientesController(db).get_all_clientes()

# Função para rodar o servidor com uvicorn
def runserver():
    uvicorn.run("main:app")

# Executa o servidor se o script for chamado diretamente
if __name__ == '__main__':
    runserver()
