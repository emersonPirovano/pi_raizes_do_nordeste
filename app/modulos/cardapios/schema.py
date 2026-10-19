
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class CardapioBase(BaseModel):
    nome: str = Field(
        min_length=2,
        max_length=100,
    )


class CardapioCreate(CardapioBase):
    loja_id: int = Field(gt=0)


class CardapioUpdate(BaseModel):
    nome: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )


class CardapioStatusUpdate(BaseModel):
    ativo: bool


class CardapioResponse(CardapioBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    loja_id: int
    ativo: bool
    criado_em: datetime


class CardapioProdutoBase(BaseModel):
    preco: Decimal = Field(
        gt=0,
        max_digits=10,
        decimal_places=2,
    )

    disponivel: bool = True


class CardapioProdutoCreate(CardapioProdutoBase):
    produto_id: int = Field(gt=0)


class CardapioProdutoUpdate(BaseModel):
    preco: Decimal | None = Field(
        default=None,
        gt=0,
        max_digits=10,
        decimal_places=2,
    )

    disponivel: bool | None = None


class CardapioProdutoResponse(CardapioProdutoBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    cardapio_id: int
    produto_id: int
