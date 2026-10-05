from sqlalchemy.orm import Session

from app.modulos.lojas.model_db import Loja


def criar_loja(db: Session, dados: dict) -> Loja:
    loja = Loja(**dados)

    db.add(loja)
    db.commit()
    db.refresh(loja)

    return loja


def listar_lojas(db: Session) -> list[Loja]:
    return db.query(Loja).order_by(Loja.id).all()


def buscar_loja_por_id(db: Session, loja_id: int) -> Loja | None:
    return db.query(Loja).filter(
        Loja.id == loja_id
    ).first()


def atualizar_loja(db: Session, loja: Loja, dados: dict) -> Loja:
    for campo, valor in dados.items():
        setattr(loja, campo, valor)

    db.commit()
    db.refresh(loja)

    return loja


def alterar_status(db: Session, loja: Loja, ativa: bool) -> Loja:
    loja.ativa = ativa

    db.commit()
    db.refresh(loja)

    return loja
