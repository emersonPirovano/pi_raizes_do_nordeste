from datetime import datetime

from sqlalchemy import (
    String,
    Integer,
    Boolean,
    DateTime,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Loja(Base):

    __tablename__ = "lojas"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    nome: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    cnpj: Mapped[str] = mapped_column(
        String(14),
        unique=True,
        nullable=False,
        index=True
    )

    telefone: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True
    )

    email: Mapped[str | None] = mapped_column(
        String(120),
        nullable=True
    )

    cep: Mapped[str | None] = mapped_column(
        String(8),
        nullable=True
    )

    logradouro: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True
    )

    numero: Mapped[str | None] = mapped_column(
        String(8),
        nullable=True
    )

    complemento: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    bairro: Mapped[str | None] = mapped_column(
        String(60),
        nullable=True
    )

    cidade: Mapped[str | None] = mapped_column(
        String(60),
        nullable=True
    )

    uf: Mapped[str | None] = mapped_column(
        String(2),
        nullable=True
    )

    ativa: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )

    criada_em: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )
