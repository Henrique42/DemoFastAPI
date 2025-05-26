# Importa as funções para criar o mecanismo de conexão com o banco de dados e iniciar sessões
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Importa o módulo os para acessar variáveis de ambiente
import os

# Importa funções da biblioteca dotenv para carregar variáveis de ambiente de um arquivo .env
from dotenv import load_dotenv, dotenv_values
load_dotenv() 

# Obtém a URL de conexão com o banco de dados da variável de ambiente DATABASE_URL
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Cria o mecanismo de conexão (engine) com o banco de dados usando a URL obtida
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Cria uma fábrica de sessões do SQLAlchemy com a engine configurada
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Função geradora que fornece uma sessão de banco de dados
def get_db():
    db = SessionLocal()  # Cria uma nova sessão
    try:
        yield db         # "Entrega" a sessão para uso temporário
    finally:
        db.close()       # Garante que a sessão será fechada após o uso
