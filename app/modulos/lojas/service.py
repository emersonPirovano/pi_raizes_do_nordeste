from sqlalchemy.orm import Session

from fastapi import HTTPException, status

from app.modulos.lojas import repository
from app.modulos.lojas.model_db import Loja


def criar_loja(db: Session, dados: dict) -> Loja:

    loja_existente = db.query(Loja).filter(
        Loja.cnpj == dados["cnpj"]
    ).first()

    if loja_existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Já existe uma loja cadastrada com este CNPJ."
        )

    return repository.criar_loja(db, dados)


def listar_lojas(db: Session) -> list[Loja]:
    return repository.listar_lojas(db)


def buscar_loja(db: Session, loja_id: int) -> Loja:

    loja = repository.buscar_loja_por_id(db, loja_id)

    if not loja:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Loja não encontrada."
        )

    return loja


def atualizar_loja(
    db: Session,
    loja_id: int,
    dados: dict
) -> Loja:

    loja = buscar_loja(db, loja_id)

    return repository.atualizar_loja(
        db,
        loja,
        dados
    )


def alterar_status(
    db: Session,
    loja_id: int,
    ativa: bool
) -> Loja:

    loja = buscar_loja(db, loja_id)

    return repository.alterar_status(
        db,
        loja,
        ativa
    )
