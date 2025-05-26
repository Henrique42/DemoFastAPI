# Importa os tipos de colunas do SQLAlchemy
from sqlalchemy import Column, Float, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

# Define a classe Clientes, que representa a tabela 'clientes' no banco de dados
class ClienteOrm(Base):
    # Define o nome da tabela no banco de dados
    __tablename__ = "clientes"

    # Atributos da tabela 'clientes'
    id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    nome = Column(String(50), index=True, nullable=False)
    email = Column(String(50), unique=True, index=True, nullable=False)
    cpf = Column(String(14), unique=True, index=True, nullable=False)
    ativo = Column(Boolean, default=True)


# Define a classe ProdutoOrm, que representa a tabela 'produtos' no banco de dados
class ProdutoOrm(Base):
    __tablename__ = "produtos"

    # Atributos da tabela 'produtos'
    id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    nome = Column(String(50), index=True, nullable=False)
    descricao = Column(String(255), nullable=False) 
    preco = Column(Float, nullable=False)
    cod_barras = Column(String(13), index=True, unique=True, nullable=False)  # Código de barras geralmente é string (ex: EAN-13)
    secao = Column(String(50), index=True, nullable=True)  # Ex: "Alimentos", "Limpeza"
    estoque = Column(Integer, default=0, nullable=False)  # Quantidade em estoque
    data_validade = Column(Date, nullable=True)  # Data de validade, pode ser nula (ex: produtos não perecíveis)

    imagens = relationship("ProdutoImagemOrm", back_populates="produto", cascade="all, delete-orphan")


class ProdutoImagemOrm(Base):
    __tablename__ = "produto_imagens"

    id = Column(Integer, primary_key=True, autoincrement=True)
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)
    url = Column(String(500), nullable=False)  # URL da imagem armazenada, ex: no S3 ou CDN

    produto = relationship("ProdutoOrm", back_populates="imagens")
