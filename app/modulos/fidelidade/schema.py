
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


TipoMovimentacao = Literal[
    "CREDITO",
    "DEBITO"
]


class FidelidadeCreate(BaseModel):
    cliente_id: int = Field(gt=0)


class FidelidadeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    cliente_id: int
    saldo_pontos: int
    criado_em: datetime
    atualizado_em: datetime


class ResgatePontosCreate(BaseModel):
    quantidade_pontos: int = Field(
        ge=100,
        description="Quantidade mínima para resgate: 100 pontos."
    )

    descricao: str | None = Field(
        default=None,
        max_length=255
    )


class MovimentacaoPontosResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    fidelidade_id: int
    pedido_id: int | None
    tipo: TipoMovimentacao
    quantidade_pontos: int
    descricao: str | None
    criado_em: datetime


class SaldoPontosResponse(BaseModel):
    cliente_id: int
    saldo_pontos: int
