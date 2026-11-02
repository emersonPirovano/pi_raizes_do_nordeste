
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Numeric,
    UniqueConstraint,
    CheckConstraint,
    func,
)

from app.db.database import Base


class Fidelidade(Base):
    __tablename__ = "fidelidade"

    __table_args__ = (
        UniqueConstraint(
            "cliente_id",
            name="uq_fidelidade_cliente"
        ),
        CheckConstraint(
            "saldo_pontos >= 0",
            name="ck_fidelidade_saldo"
        ),
    )

    id = Column(Integer, primary_key=True, index=True)

    cliente_id = Column(
        Integer,
        ForeignKey("clientes.id"),
        nullable=False
    )

    saldo_pontos = Column(
        Integer,
        nullable=False,
        default=0
    )

    criado_em = Column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )

    atualizado_em = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now()
    )


class MovimentacaoPontos(Base):
    __tablename__ = "movimentacao_pontos"

    __table_args__ = (
        CheckConstraint(
            "quantidade_pontos > 0",
            name="ck_movimentacao_quantidade"
        ),
        CheckConstraint(
            "tipo IN ('CREDITO', 'DEBITO')",
            name="ck_movimentacao_tipo"
        ),
        UniqueConstraint(
            "pedido_id",
            name="uq_movimentacao_pedido"
        ),
    )

    id = Column(Integer, primary_key=True, index=True)

    fidelidade_id = Column(
        Integer,
        ForeignKey("fidelidade.id"),
        nullable=False
    )

    pedido_id = Column(
        Integer,
        ForeignKey("pedidos.id"),
        nullable=True
    )

    tipo = Column(
        String(10),
        nullable=False
    )

    quantidade_pontos = Column(
        Integer,
        nullable=False
    )

    descricao = Column(
        String(255),
        nullable=True
    )

    criado_em = Column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )
