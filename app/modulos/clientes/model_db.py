
from datetime import date

from sqlalchemy import Boolean, Date, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Cliente(Base):
    __tablename__ = "clientes"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    nome: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    email: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
        index=True,
    )

    telefone: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    data_nascimento: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    consentimento_lgpd: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )
