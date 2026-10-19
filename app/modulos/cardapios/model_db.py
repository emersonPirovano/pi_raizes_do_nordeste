
from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Cardapio(Base):
    __tablename__ = "cardapios"

    __table_args__ = (
        UniqueConstraint(
            "loja_id",
            name="uq_cardapios_loja",
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    nome: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    ativo: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    loja_id: Mapped[int] = mapped_column(
        ForeignKey("lojas.id"),
        nullable=False,
        index=True,
    )

    criado_em: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
    )


class CardapioProduto(Base):
    __tablename__ = "cardapio_produto"

    __table_args__ = (
        UniqueConstraint(
            "cardapio_id",
            "produto_id",
            name="uq_cardapio_produto",
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    cardapio_id: Mapped[int] = mapped_column(
        ForeignKey("cardapios.id"),
        nullable=False,
        index=True,
    )

    produto_id: Mapped[int] = mapped_column(
        ForeignKey("produtos.id"),
        nullable=False,
        index=True,
    )

    preco: Mapped[float] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    disponivel: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )
