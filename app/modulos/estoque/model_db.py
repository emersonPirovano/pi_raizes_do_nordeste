
from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Estoque(Base):
    __tablename__ = "estoque"

    __table_args__ = (
        UniqueConstraint(
            "loja_id",
            "produto_id",
            name="uq_estoque_loja_produto",
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    loja_id: Mapped[int] = mapped_column(
        ForeignKey("lojas.id"),
        nullable=False,
        index=True,
    )

    produto_id: Mapped[int] = mapped_column(
        ForeignKey("produtos.id"),
        nullable=False,
        index=True,
    )

    quantidade: Mapped[Decimal] = mapped_column(
        Numeric(12, 3),
        nullable=False,
        default=0,
    )

    quantidade_minima: Mapped[Decimal] = mapped_column(
        Numeric(12, 3),
        nullable=False,
        default=0,
    )

    atualizado_em: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
