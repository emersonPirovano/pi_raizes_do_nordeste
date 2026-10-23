
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modulos.estoque.model_db import Estoque


def criar_estoque(
    db: Session,
    loja_id: int,
    produto_id: int,
    quantidade: Decimal = Decimal("0"),
    quantidade_minima: Decimal = Decimal("0"),
) -> Estoque:
    estoque = Estoque(
        loja_id=loja_id,
        produto_id=produto_id,
        quantidade=quantidade,
        quantidade_minima=quantidade_minima,
    )

    db.add(estoque)
    db.commit()
    db.refresh(estoque)

    return estoque


def listar_estoques(
    db: Session,
    loja_id: int | None = None,
    produto_id: int | None = None,
    apenas_baixo: bool = False,
) -> list[Estoque]:
    consulta = select(Estoque)

    if loja_id is not None:
        consulta = consulta.where(Estoque.loja_id == loja_id)

    if produto_id is not None:
        consulta = consulta.where(Estoque.produto_id == produto_id)

    if apenas_baixo:
        consulta = consulta.where(
            Estoque.quantidade <= Estoque.quantidade_minima
        )

    consulta = consulta.order_by(Estoque.id)

    return list(db.scalars(consulta).all())


def buscar_estoque_por_id(
    db: Session,
    estoque_id: int,
) -> Estoque | None:
    return db.get(Estoque, estoque_id)


def buscar_estoque_por_produto(
    db: Session,
    loja_id: int,
    produto_id: int,
) -> Estoque | None:
    consulta = select(Estoque).where(
        Estoque.loja_id == loja_id,
        Estoque.produto_id == produto_id,
    )

    return db.scalars(consulta).first()


def atualizar_estoque(
    db: Session,
    estoque: Estoque,
    quantidade: Decimal | None = None,
    quantidade_minima: Decimal | None = None,
) -> Estoque:
    if quantidade is not None:
        estoque.quantidade = quantidade

    if quantidade_minima is not None:
        estoque.quantidade_minima = quantidade_minima

    db.commit()
    db.refresh(estoque)

    return estoque


def excluir_estoque(
    db: Session,
    estoque: Estoque,
) -> None:
    db.delete(estoque)
    db.commit()
