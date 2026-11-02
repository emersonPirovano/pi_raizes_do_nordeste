
from sqlalchemy.orm import Session

from app.modulos.fidelidade.model_db import (
    Fidelidade,
    MovimentacaoPontos,
)


#cadastro

def criar_fidelidade(db: Session, dados: dict):
    fidelidade = Fidelidade(**dados)

    db.add(fidelidade)
    db.flush()

    return fidelidade


def buscar_fidelidade_por_id(
    db: Session,
    fidelidade_id: int
):
    return db.query(Fidelidade).filter(
        Fidelidade.id == fidelidade_id
    ).first()


def buscar_fidelidade_por_cliente(
    db: Session,
    cliente_id: int
):
    return db.query(Fidelidade).filter(
        Fidelidade.cliente_id == cliente_id
    ).first()


def listar_fidelidades(db: Session):
    return db.query(Fidelidade).order_by(
        Fidelidade.id.desc()
    ).all()


#saldo

def atualizar_saldo(
    db: Session,
    fidelidade: Fidelidade,
    novo_saldo: int
):
    fidelidade.saldo_pontos = novo_saldo
    db.flush()

    return fidelidade


#movimentações

def criar_movimentacao(
    db: Session,
    dados: dict
):
    movimentacao = MovimentacaoPontos(**dados)

    db.add(movimentacao)
    db.flush()

    return movimentacao


def buscar_movimentacao_por_id(
    db: Session,
    movimentacao_id: int
):
    return db.query(MovimentacaoPontos).filter(
        MovimentacaoPontos.id == movimentacao_id
    ).first()


def buscar_movimentacao_por_pedido(
    db: Session,
    pedido_id: int
):
    return db.query(MovimentacaoPontos).filter(
        MovimentacaoPontos.pedido_id == pedido_id
    ).first()


def listar_movimentacoes(
    db: Session,
    fidelidade_id: int
):
    return db.query(MovimentacaoPontos).filter(
        MovimentacaoPontos.fidelidade_id == fidelidade_id
    ).order_by(
        MovimentacaoPontos.criado_em.desc()
    ).all()
