# Importa a função para criar uma classe base para os modelos ORM
from sqlalchemy.ext.declarative import declarative_base

# Importa os tipos de colunas do SQLAlchemy
from sqlalchemy import Column, Integer, String, Boolean

# Cria a classe base que será usada como superclasse para os modelos
Base = declarative_base()

# Define a classe Clientes, que representa a tabela 'clientes' no banco de dados
class Clientes(Base):
    # Define o nome da tabela no banco de dados
    __tablename__ = "clientes"

    # Atributos da tabela 'clientes'
    id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    nome = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    cpf = Column(String, unique=True, index=True, nullable=False)
    ativo = Column(Boolean, default=True)
