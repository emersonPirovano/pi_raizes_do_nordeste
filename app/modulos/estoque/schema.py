
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class EstoqueBase(BaseModel):
    quantidade: Decimal = Field(
        default=Decimal("0"),
        ge=0,
        max_digits=12,
        decimal_places=3,
    )

    quantidade_minima: Decimal = Field(
        default=Decimal("0"),
        ge=0,
        max_digits=12,
        decimal_places=3,
    )


class EstoqueCreate(EstoqueBase):
    loja_id: int = Field(gt=0)
    produto_id: int = Field(gt=0)


class EstoqueUpdate(BaseModel):
    quantidade: Decimal | None = Field(
        default=None,
        ge=0,
        max_digits=12,
        decimal_places=3,
    )

    quantidade_minima: Decimal | None = Field(
        default=None,
        ge=0,
        max_digits=12,
        decimal_places=3,
    )


class EstoqueResponse(EstoqueBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    loja_id: int
    produto_id: int
    atualizado_em: datetime
