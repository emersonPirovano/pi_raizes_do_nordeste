
from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Produto(Base):
    __tablename__ = "produtos"

    __table_args__ = (
        UniqueConstraint(
            "loja_id",
            "codigo",
            name="uq_produtos_loja_codigo",
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

    nome: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
        index=True,
    )

    descricao: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    codigo: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    preco: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    custo: Mapped[Decimal | None] = mapped_column(
        Numeric(10, 2),
        nullable=True,
    )

    categoria: Mapped[str | None] = mapped_column(
        String(80),
        nullable=True,
    )

    unidade_medida: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="un",
    )

    ativo: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    criado_em: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
    )
