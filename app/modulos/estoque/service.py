
from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.modulos.estoque import repository
from app.modulos.lojas.model_db import Loja
from app.modulos.produtos.model_db import Produto


def validar_loja_e_produto(
    db: Session,
    loja_id: int,
    produto_id: int,
) -> None:
    loja = db.get(Loja, loja_id)

    if loja is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Loja não encontrada.",
        )

    if not loja.ativa:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não é possível cadastrar estoque para uma loja inativa.",
        )

    produto = db.get(Produto, produto_id)

    if produto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado.",
        )

    if produto.loja_id != loja_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O produto não pertence à loja informada.",
        )

    if not produto.ativo:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não é possível cadastrar estoque para um produto inativo.",
        )


def criar_estoque(
    db: Session,
    loja_id: int,
    produto_id: int,
    quantidade: Decimal = Decimal("0"),
    quantidade_minima: Decimal = Decimal("0"),
):
    validar_loja_e_produto(db, loja_id, produto_id)

    estoque_existente = repository.buscar_estoque_por_produto(
        db,
        loja_id,
        produto_id,
    )

    if estoque_existente is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Já existe um registro de estoque para este produto nesta loja.",
        )

    return repository.criar_estoque(
        db=db,
        loja_id=loja_id,
        produto_id=produto_id,
        quantidade=quantidade,
        quantidade_minima=quantidade_minima,
    )


def listar_estoques(
    db: Session,
    loja_id: int | None = None,
    produto_id: int | None = None,
    apenas_baixo: bool = False,
):
    if loja_id is not None and db.get(Loja, loja_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Loja não encontrada.",
        )

    if produto_id is not None:
        produto = db.get(Produto, produto_id)

        if produto is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Produto não encontrado.",
            )

        if loja_id is not None and produto.loja_id != loja_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="O produto não pertence à loja informada.",
            )

    return repository.listar_estoques(
        db=db,
        loja_id=loja_id,
        produto_id=produto_id,
        apenas_baixo=apenas_baixo,
    )


def buscar_estoque_por_id(
    db: Session,
    estoque_id: int,
):
    estoque = repository.buscar_estoque_por_id(db, estoque_id)

    if estoque is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registro de estoque não encontrado.",
        )

    return estoque


def atualizar_estoque(
    db: Session,
    estoque_id: int,
    quantidade: Decimal | None = None,
    quantidade_minima: Decimal | None = None,
):
    estoque = buscar_estoque_por_id(db, estoque_id)

    if quantidade is None and quantidade_minima is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Informe a quantidade ou a quantidade mínima para atualizar.",
        )

    return repository.atualizar_estoque(
        db=db,
        estoque=estoque,
        quantidade=quantidade,
        quantidade_minima=quantidade_minima,
    )


def excluir_estoque(
    db: Session,
    estoque_id: int,
) -> None:
    estoque = buscar_estoque_por_id(db, estoque_id)

    repository.excluir_estoque(db, estoque)
