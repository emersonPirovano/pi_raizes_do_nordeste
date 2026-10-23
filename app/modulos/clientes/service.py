
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.modulos.clientes import repository
from app.modulos.clientes.model_db import Cliente


def criar_cliente(
    db: Session,
    dados: dict,
) -> Cliente:
    email = dados.get("email")

    if email:
        cliente_existente = repository.buscar_cliente_por_email(
            db,
            email,
        )

        if cliente_existente is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Já existe um cliente cadastrado com este e-mail.",
            )

    return repository.criar_cliente(db, dados)


def listar_clientes(
    db: Session,
) -> list[Cliente]:
    return repository.listar_clientes(db)


def buscar_cliente_por_id(
    db: Session,
    cliente_id: int,
) -> Cliente:
    cliente = repository.buscar_cliente_por_id(
        db,
        cliente_id,
    )

    if cliente is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não encontrado.",
        )

    return cliente


def atualizar_cliente(
    db: Session,
    cliente_id: int,
    dados: dict,
) -> Cliente:
    cliente = buscar_cliente_por_id(db, cliente_id)

    email_novo = dados.get("email")

    if email_novo:
        cliente_email = repository.buscar_cliente_por_email(
            db,
            email_novo,
        )

        if (
            cliente_email is not None
            and cliente_email.id != cliente.id
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Este e-mail já está cadastrado para outro cliente.",
            )

    return repository.atualizar_cliente(
        db,
        cliente,
        dados,
    )


def excluir_cliente(
    db: Session,
    cliente_id: int,
) -> None:
    cliente = buscar_cliente_por_id(db, cliente_id)

    repository.excluir_cliente(db, cliente)
