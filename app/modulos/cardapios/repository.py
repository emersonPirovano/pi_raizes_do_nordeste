
from decimal import Decimal

from sqlalchemy.orm import Session

from app.modulos.cardapios.model_db import Cardapio, CardapioProduto
from app.modulos.cardapios.schema import (
    CardapioCreate,
    CardapioUpdate,
    CardapioProdutoCreate,
    CardapioProdutoUpdate,
)


#Cardápio

def criar_cardapio(
    db: Session,
    dados: CardapioCreate,
) -> Cardapio:
    cardapio = Cardapio(**dados.model_dump())

    db.add(cardapio)
    db.commit()
    db.refresh(cardapio)

    return cardapio


def listar_cardapios(
    db: Session,
    incluir_inativos: bool = False,
) -> list[Cardapio]:
    consulta = db.query(Cardapio)

    if not incluir_inativos:
        consulta = consulta.filter(Cardapio.ativo.is_(True))

    return consulta.order_by(Cardapio.nome.asc()).all()


def buscar_cardapio_por_id(
    db: Session,
    cardapio_id: int,
) -> Cardapio | None:
    return (
        db.query(Cardapio)
        .filter(Cardapio.id == cardapio_id)
        .first()
    )


def buscar_cardapio_por_loja(
    db: Session,
    loja_id: int,
) -> Cardapio | None:
    return (
        db.query(Cardapio)
        .filter(Cardapio.loja_id == loja_id)
        .first()
    )


def atualizar_cardapio(
    db: Session,
    cardapio: Cardapio,
    dados: CardapioUpdate,
) -> Cardapio:
    campos = dados.model_dump(exclude_unset=True)

    for campo, valor in campos.items():
        setattr(cardapio, campo, valor)

    db.commit()
    db.refresh(cardapio)

    return cardapio


def alterar_status_cardapio(
    db: Session,
    cardapio: Cardapio,
    ativo: bool,
) -> Cardapio:
    cardapio.ativo = ativo

    db.commit()
    db.refresh(cardapio)

    return cardapio


# Produtos

def adicionar_produto(
    db: Session,
    cardapio_id: int,
    dados: CardapioProdutoCreate,
) -> CardapioProduto:
    item = CardapioProduto(
        cardapio_id=cardapio_id,
        **dados.model_dump(),
    )

    db.add(item)
    db.commit()
    db.refresh(item)

    return item


def listar_produtos_cardapio(
    db: Session,
    cardapio_id: int,
    incluir_indisponiveis: bool = False,
) -> list[CardapioProduto]:
    consulta = db.query(CardapioProduto).filter(
        CardapioProduto.cardapio_id == cardapio_id
    )

    if not incluir_indisponiveis:
        consulta = consulta.filter(
            CardapioProduto.disponivel.is_(True)
        )

    return consulta.order_by(CardapioProduto.id.asc()).all()


def buscar_item_cardapio(
    db: Session,
    cardapio_id: int,
    produto_id: int,
) -> CardapioProduto | None:
    return (
        db.query(CardapioProduto)
        .filter(
            CardapioProduto.cardapio_id == cardapio_id,
            CardapioProduto.produto_id == produto_id,
        )
        .first()
    )


def atualizar_item_cardapio(
    db: Session,
    item: CardapioProduto,
    dados: CardapioProdutoUpdate,
) -> CardapioProduto:
    campos = dados.model_dump(exclude_unset=True)

    for campo, valor in campos.items():
        setattr(item, campo, valor)

    db.commit()
    db.refresh(item)

    return item


def remover_item_cardapio(
    db: Session,
    item: CardapioProduto,
) -> None:
    db.delete(item)
    db.commit()
