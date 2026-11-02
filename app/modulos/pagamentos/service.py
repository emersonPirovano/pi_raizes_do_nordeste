
from decimal import Decimal, ROUND_HALF_UP

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.modulos.pagamentos import repository
from app.modulos.pedidos.model_db import Pedido


def calcular_valor(valor):
    return Decimal(str(valor)).quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP
    )


def buscar_pedido(db: Session, pedido_id: int):
    pedido = db.query(Pedido).filter(
        Pedido.id == pedido_id
    ).first()

    if not pedido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pedido não encontrado."
        )

    return pedido


def validar_pedido_para_pagamento(pedido: Pedido):
    if pedido.status.upper() == "CANCELADO":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não é permitido pagar um pedido cancelado."
        )

    if pedido.status.upper() != "PENDENTE":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O pedido não está disponível para pagamento."
        )


def criar_pagamento(db: Session, dados: dict):

    pedido = buscar_pedido(db, dados["pedido_id"])

    validar_pedido_para_pagamento(pedido)

    pagamento_existente = repository.buscar_pagamento_por_pedido(
        db,
        pedido.id
    )

    if pagamento_existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Este pedido já possui um pagamento registrado."
        )

    valor_pagamento = calcular_valor(dados["valor"])
    valor_pedido = calcular_valor(pedido.valor_total)

    if valor_pagamento != valor_pedido:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O valor do pagamento deve corresponder ao valor total do pedido."
        )

    dados_pagamento = {
        "pedido_id": pedido.id,
        "forma_pagamento": dados["forma_pagamento"],
        "valor": valor_pedido,
        "status": "PENDENTE"
    }

    try:
        return repository.criar_pagamento(db, dados_pagamento)

    except Exception:
        db.rollback()
        raise


def listar_pagamentos(
    db: Session,
    pedido_id: int | None = None,
    status_pagamento: str | None = None
):
    if pedido_id is not None:
        buscar_pedido(db, pedido_id)

    return repository.listar_pagamentos(
        db,
        pedido_id=pedido_id,
        status=status_pagamento
    )


def buscar_pagamento_por_id(
    db: Session,
    pagamento_id: int
):
    pagamento = repository.buscar_pagamento_por_id(
        db,
        pagamento_id
    )

    if not pagamento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pagamento não encontrado."
        )

    return pagamento


def buscar_pagamento_por_pedido(
    db: Session,
    pedido_id: int
):
    buscar_pedido(db, pedido_id)

    pagamento = repository.buscar_pagamento_por_pedido(
        db,
        pedido_id
    )

    if not pagamento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pagamento não encontrado para este pedido."
        )

    return pagamento


def atualizar_status(
    db: Session,
    pagamento_id: int,
    novo_status: str
):
    pagamento = buscar_pagamento_por_id(db, pagamento_id)

    if pagamento.status != "PENDENTE":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Somente pagamentos pendentes podem ter o status alterado."
        )

    try:
        pagamento = repository.atualizar_status(
            db,
            pagamento,
            novo_status
        )

        if novo_status == "APROVADO":
            pedido = buscar_pedido(db, pagamento.pedido_id)
            pedido.status = "PAGO"
            db.commit()

        return pagamento

    except Exception:
        db.rollback()
        raise
