
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.modulos.fidelidade import repository
from app.modulos.clientes.model_db import Cliente
from app.modulos.pedidos.model_db import Pedido
from app.modulos.pagamentos.model_db import Pagamento


VALOR_POR_PONTO = 1
RESGATE_MINIMO = 100


def buscar_cliente(db: Session, cliente_id: int):
    cliente = db.query(Cliente).filter(
        Cliente.id == cliente_id
    ).first()

    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não encontrado."
        )

    return cliente


def buscar_fidelidade(db: Session, cliente_id: int):
    fidelidade = repository.buscar_fidelidade_por_cliente(
        db,
        cliente_id
    )

    if not fidelidade:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não possui cadastro no programa de fidelidade."
        )

    return fidelidade


#cadastro

def criar_fidelidade(db: Session, cliente_id: int):
    buscar_cliente(db, cliente_id)

    existente = repository.buscar_fidelidade_por_cliente(
        db,
        cliente_id
    )

    if existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cliente já possui cadastro no programa de fidelidade."
        )

    try:
        fidelidade = repository.criar_fidelidade(
            db,
            {
                "cliente_id": cliente_id,
                "saldo_pontos": 0
            }
        )

        db.commit()
        db.refresh(fidelidade)

        return fidelidade

    except Exception:
        db.rollback()
        raise


#consulta de saldo

def consultar_saldo(db: Session, cliente_id: int):
    fidelidade = buscar_fidelidade(db, cliente_id)

    return {
        "cliente_id": cliente_id,
        "saldo_pontos": fidelidade.saldo_pontos
    }


#creditar pontos

def creditar_pontos_por_pedido(
    db: Session,
    pedido_id: int
):
    pedido = db.query(Pedido).filter(
        Pedido.id == pedido_id
    ).first()

    if not pedido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pedido não encontrado."
        )

    pagamento = db.query(Pagamento).filter(
        Pagamento.pedido_id == pedido_id
    ).first()

    if not pagamento or pagamento.status != "APROVADO":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O pagamento do pedido não está aprovado."
        )

    movimentacao_existente = (
        repository.buscar_movimentacao_por_pedido(
            db,
            pedido_id
        )
    )

    if movimentacao_existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Este pedido já possui movimentação de pontos."
        )

    fidelidade = buscar_fidelidade(db, pedido.cliente_id)

    pontos = int(pagamento.valor // VALOR_POR_PONTO)

    if pontos <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O pedido não gera pontos."
        )

    try:
        repository.atualizar_saldo(
            db,
            fidelidade,
            fidelidade.saldo_pontos + pontos
        )

        movimentacao = repository.criar_movimentacao(
            db,
            {
                "fidelidade_id": fidelidade.id,
                "pedido_id": pedido_id,
                "tipo": "CREDITO",
                "quantidade_pontos": pontos,
                "descricao": f"Crédito referente ao pedido {pedido_id}"
            }
        )

        db.commit()
        db.refresh(movimentacao)

        return movimentacao

    except Exception:
        db.rollback()
        raise


#resgate

def resgatar_pontos(
    db: Session,
    cliente_id: int,
    quantidade_pontos: int,
    descricao: str | None = None
):
    if quantidade_pontos < RESGATE_MINIMO:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"O resgate mínimo é de {RESGATE_MINIMO} pontos."
        )

    fidelidade = buscar_fidelidade(db, cliente_id)

    if fidelidade.saldo_pontos < quantidade_pontos:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Saldo de pontos insuficiente."
        )

    try:
        repository.atualizar_saldo(
            db,
            fidelidade,
            fidelidade.saldo_pontos - quantidade_pontos
        )

        movimentacao = repository.criar_movimentacao(
            db,
            {
                "fidelidade_id": fidelidade.id,
                "pedido_id": None,
                "tipo": "DEBITO",
                "quantidade_pontos": quantidade_pontos,
                "descricao": descricao or "Resgate de pontos"
            }
        )

        db.commit()
        db.refresh(movimentacao)

        return movimentacao

    except Exception:
        db.rollback()
        raise


#extrato

def listar_movimentacoes(
    db: Session,
    cliente_id: int
):
    fidelidade = buscar_fidelidade(db, cliente_id)

    return repository.listar_movimentacoes(
        db,
        fidelidade.id
    )

def listar_fidelidades(db: Session):
    return repository.listar_fidelidades(db)
