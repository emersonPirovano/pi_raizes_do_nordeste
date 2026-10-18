
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ProdutoBase(BaseModel):
    nome: str = Field(
        min_length=2,
        max_length=120,
    )

    descricao: str | None = None

    codigo: str | None = Field(
        default=None,
        max_length=50,
    )

    preco: Decimal = Field(
        gt=0,
        max_digits=10,
        decimal_places=2,
    )

    custo: Decimal | None = Field(
        default=None,
        ge=0,
        max_digits=10,
        decimal_places=2,
    )

    categoria: str | None = Field(
        default=None,
        max_length=80,
    )

    unidade_medida: str = Field(
        default="un",
        min_length=1,
        max_length=20,
    )


class ProdutoCreate(ProdutoBase):
    loja_id: int = Field(gt=0)


class ProdutoUpdate(BaseModel):
    nome: str | None = Field(
        default=None,
        min_length=2,
        max_length=120,
    )

    descricao: str | None = None

    codigo: str | None = Field(
        default=None,
        max_length=50,
    )

    preco: Decimal | None = Field(
        default=None,
        gt=0,
        max_digits=10,
        decimal_places=2,
    )

    custo: Decimal | None = Field(
        default=None,
        ge=0,
        max_digits=10,
        decimal_places=2,
    )

    categoria: str | None = Field(
        default=None,
        max_length=80,
    )

    unidade_medida: str | None = Field(
        default=None,
        min_length=1,
        max_length=20,
    )


class ProdutoStatusUpdate(BaseModel):
    ativo: bool


class ProdutoResponse(ProdutoBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    loja_id: int
    ativo: bool
    criado_em: datetime
