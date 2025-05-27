from sqlalchemy import Column, Float, Integer, String, Boolean, Date, ForeignKey, Enum, DateTime, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum

# Enum para status do pedido
class StatusPedidoEnum(str, enum.Enum):
    PENDENTE = "pendente"
    PROCESSANDO = "processando"
    ENVIADO = "enviado"
    ENTREGUE = "entregue"
    CANCELADO = "cancelado"

class ClienteOrm(Base):
    __tablename__ = "clientes"

    id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    nome = Column(String(50), index=True, nullable=False)
    email = Column(String(50), unique=True, index=True, nullable=False)
    cpf = Column(String(14), unique=True, index=True, nullable=False)
    ativo = Column(Boolean, default=True)

    pedidos = relationship("PedidoOrm", back_populates="cliente", cascade="all, delete-orphan", passive_deletes=True)


class ProdutoOrm(Base):
    __tablename__ = "produtos"

    id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    nome = Column(String(50), index=True, nullable=False)
    descricao = Column(String(255), nullable=False)
    preco = Column(Float, nullable=False)
    cod_barras = Column(String(13), index=True, unique=True, nullable=False)
    secao = Column(String(50), index=True, nullable=True)
    estoque = Column(Integer, default=0, nullable=False)
    data_validade = Column(Date, nullable=True)

    imagens = relationship("ProdutoImagemOrm", back_populates="produto", cascade="all, delete-orphan")
    pedidos = relationship("PedidoProdutoOrm", back_populates="produto", cascade="all, delete-orphan")


class ProdutoImagemOrm(Base):
    __tablename__ = "produto_imagens"

    id = Column(Integer, primary_key=True, autoincrement=True)
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)
    url = Column(String(500), nullable=False)

    produto = relationship("ProdutoOrm", back_populates="imagens")


class PedidoOrm(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    cliente_id = Column(Integer, ForeignKey("clientes.id", ondelete="CASCADE"), nullable=False)
    
    d_pedido = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    status = Column(Enum(StatusPedidoEnum), default=StatusPedidoEnum.PENDENTE, nullable=False)
    periodo_inicio = Column(Date, nullable=True)
    periodo_fim = Column(Date, nullable=True)

    cliente = relationship("ClienteOrm", back_populates="pedidos")
    produtos = relationship("PedidoProdutoOrm", back_populates="pedido", cascade="all, delete-orphan")


class PedidoProdutoOrm(Base):
    __tablename__ = "pedido_produtos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"), nullable=False)
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)
    quantidade = Column(Integer, nullable=False, default=1)

    pedido = relationship("PedidoOrm", back_populates="produtos")
    produto = relationship("ProdutoOrm", back_populates="pedidos")
