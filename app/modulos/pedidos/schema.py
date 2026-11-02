
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

# itens do pedido

class ItemPedidoCreate(BaseModel):
    produto_id: int = Field(gt=0)
    quantidade: int = Field(gt=0)


class ItemPedidoUpdate(BaseModel):
    quantidade: int = Field(gt=0)


class ItemPedidoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    pedido_id: int
    produto_id: int
    quantidade: int
    preco_unitario: Decimal
    subtotal: Decimal

# pedido

class PedidoCreate(BaseModel):
    cliente_id: int = Field(gt=0)
    loja_id: int = Field(gt=0)
    itens: list[ItemPedidoCreate] = Field(min_length=1)


class PedidoUpdate(BaseModel):
    status: str | None = Field(
        default=None,
        min_length=3,
        max_length=30,
    )


class PedidoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    cliente_id: int
    loja_id: int
    data_hora: datetime
    status: str
    valor_total: Decimal
    itens: list[ItemPedidoResponse] = Field(default_factory=list)
