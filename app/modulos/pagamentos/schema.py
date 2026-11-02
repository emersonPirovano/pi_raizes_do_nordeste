
from datetime import datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


# Formas de pagamento permitidas
FormaPagamento = Literal[
    "DINHEIRO",
    "DEBITO",
    "CREDITO",
    "PIX"
]


# Situações possíveis do pagamento
StatusPagamento = Literal[
    "PENDENTE",
    "APROVADO",
    "RECUSADO",
    "CANCELADO"
]


class PagamentoCreate(BaseModel):
    pedido_id: int = Field(gt=0)

    forma_pagamento: FormaPagamento

    valor: Decimal = Field(gt=0, max_digits=12, decimal_places=2)


class PagamentoUpdate(BaseModel):
    status: StatusPagamento


class PagamentoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    pedido_id: int
    forma_pagamento: FormaPagamento
    valor: Decimal
    status: StatusPagamento
    criado_em: datetime
