
from sqlalchemy.orm import Session

from app.modulos.pagamentos.model_db import Pagamento


def criar_pagamento(db: Session, dados: dict):
    pagamento = Pagamento(**dados)

    db.add(pagamento)
    db.commit()
    db.refresh(pagamento)

    return pagamento


def listar_pagamentos(
    db: Session,
    pedido_id: int | None = None,
    status: str | None = None
):
    consulta = db.query(Pagamento)

    if pedido_id is not None:
        consulta = consulta.filter(
            Pagamento.pedido_id == pedido_id
        )

    if status is not None:
        consulta = consulta.filter(
            Pagamento.status == status
        )

    return consulta.order_by(Pagamento.id.desc()).all()


def buscar_pagamento_por_id(
    db: Session,
    pagamento_id: int
):
    return db.query(Pagamento).filter(
        Pagamento.id == pagamento_id
    ).first()


def buscar_pagamento_por_pedido(
    db: Session,
    pedido_id: int
):
    return db.query(Pagamento).filter(
        Pagamento.pedido_id == pedido_id
    ).first()


def atualizar_status(
    db: Session,
    pagamento: Pagamento,
    novo_status: str
):
    pagamento.status = novo_status

    db.commit()
    db.refresh(pagamento)

    return pagamento


def excluir_pagamento(
    db: Session,
    pagamento: Pagamento
):
    db.delete(pagamento)
    db.commit()
