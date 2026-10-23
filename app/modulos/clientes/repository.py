
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modulos.clientes.model_db import Cliente


def criar_cliente(
    db: Session,
    dados: dict,
) -> Cliente:
    cliente = Cliente(**dados)

    db.add(cliente)
    db.commit()
    db.refresh(cliente)

    return cliente


def listar_clientes(
    db: Session,
) -> list[Cliente]:
    consulta = select(Cliente).order_by(Cliente.id)

    return list(db.scalars(consulta).all())


def buscar_cliente_por_id(
    db: Session,
    cliente_id: int,
) -> Cliente | None:
    return db.get(Cliente, cliente_id)


def buscar_cliente_por_email(
    db: Session,
    email: str,
) -> Cliente | None:
    consulta = select(Cliente).where(
        Cliente.email == email
    )

    return db.scalars(consulta).first()


def atualizar_cliente(
    db: Session,
    cliente: Cliente,
    dados: dict,
) -> Cliente:
    for campo, valor in dados.items():
        setattr(cliente, campo, valor)

    db.commit()
    db.refresh(cliente)

    return cliente


def excluir_cliente(
    db: Session,
    cliente: Cliente,
) -> None:
    db.delete(cliente)
    db.commit()
