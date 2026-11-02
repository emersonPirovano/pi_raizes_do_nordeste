
from sqlalchemy import (
    Column,
    Integer,
    String,
    Numeric,
    DateTime,
    ForeignKey,
    UniqueConstraint,
    func,
)

from app.db.database import Base


class Pagamento(Base):
    __tablename__ = "pagamentos"

    __table_args__ = (
        UniqueConstraint(
            "pedido_id",
            name="uq_pagamentos_pedido"
        ),
    )

    id = Column(Integer, primary_key=True, index=True)

    pedido_id = Column(
        Integer,
        ForeignKey("pedidos.id"),
        nullable=False
    )

    forma_pagamento = Column(
        String(20),
        nullable=False
    )

    valor = Column(
        Numeric(12, 2),
        nullable=False
    )

    status = Column(
        String(20),
        nullable=False,
        default="PENDENTE"
    )

    criado_em = Column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )
