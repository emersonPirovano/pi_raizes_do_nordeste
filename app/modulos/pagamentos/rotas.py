
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.modulos.pagamentos import service
from app.modulos.pagamentos.schema import (
    PagamentoCreate,
    PagamentoUpdate,
    PagamentoResponse,
)

router = APIRouter(
    prefix="/pagamentos",
    tags=["Pagamentos"]
)

#Registra o pagamento

@router.post(
    "/",
    response_model=PagamentoResponse,
    status_code=status.HTTP_201_CREATED
)
def criar_pagamento(
    dados: PagamentoCreate,
    db: Session = Depends(get_db)
):
    return service.criar_pagamento(
        db,
        dados.model_dump()
    )

#Lista o pagamento

@router.get("/", response_model=list[PagamentoResponse])
def listar_pagamentos(
    pedido_id: int | None = Query(None, gt=0),
    status_pagamento: str | None = Query(None),
    db: Session = Depends(get_db)
):
    return service.listar_pagamentos(
        db,
        pedido_id=pedido_id,
        status_pagamento=status_pagamento
    )


#Busca o pagamento

@router.get(
    "/pedido/{pedido_id}",
    response_model=PagamentoResponse
)
def buscar_pagamento_por_pedido(
    pedido_id: int,
    db: Session = Depends(get_db)
):
    return service.buscar_pagamento_por_pedido(
        db,
        pedido_id
    )


@router.get(
    "/{pagamento_id}",
    response_model=PagamentoResponse
)
def buscar_pagamento(
    pagamento_id: int,
    db: Session = Depends(get_db)
):
    return service.buscar_pagamento_por_id(
        db,
        pagamento_id
    )


#Atualiza status do pagamento

@router.patch(
    "/{pagamento_id}/status",
    response_model=PagamentoResponse
)
def atualizar_status(
    pagamento_id: int,
    dados: PagamentoUpdate,
    db: Session = Depends(get_db)
):
    return service.atualizar_status(
        db,
        pagamento_id,
        dados.status
    )
