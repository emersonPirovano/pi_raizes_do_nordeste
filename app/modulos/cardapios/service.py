
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.modulos.lojas.model_db import Loja
from app.modulos.produtos.model_db import Produto
from app.modulos.cardapios import repository
from app.modulos.cardapios.model_db import Cardapio, CardapioProduto
from app.modulos.cardapios.schema import (
    CardapioCreate,
    CardapioUpdate,
    CardapioProdutoCreate,
    CardapioProdutoUpdate,
)

def verificar_loja(
    db: Session,
    loja_id: int,
) -> Loja:
    loja = (
        db.query(Loja)
        .filter(Loja.id == loja_id)
        .first()
    )

    if loja is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Loja não encontrada.",
        )

    if not loja.ativa:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A loja está inativa.",
        )

    return loja


def verificar_cardapio(
    db: Session,
    cardapio_id: int,
) -> Cardapio:
    cardapio = repository.buscar_cardapio_por_id(
        db,
        cardapio_id,
    )

    if cardapio is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cardápio não encontrado.",
        )

    return cardapio


def verificar_produto(
    db: Session,
    produto_id: int,
    loja_id: int,
) -> Produto:
    produto = (
        db.query(Produto)
        .filter(Produto.id == produto_id)
        .first()
    )

    if produto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado.",
        )

    if produto.loja_id != loja_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O produto não pertence à loja deste cardápio.",
        )

    if not produto.ativo:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não é possível adicionar um produto inativo.",
        )

    return produto


#cardápio

def criar_cardapio(
    db: Session,
    dados: CardapioCreate,
) -> Cardapio:
    verificar_loja(db, dados.loja_id)

    cardapio_existente = repository.buscar_cardapio_por_loja(
        db,
        dados.loja_id,
    )

    if cardapio_existente is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Esta loja já possui um cardápio cadastrado.",
        )

    return repository.criar_cardapio(db, dados)


def listar_cardapios(
    db: Session,
    incluir_inativos: bool = False,
) -> list[Cardapio]:
    return repository.listar_cardapios(
        db,
        incluir_inativos,
    )


def buscar_cardapio(
    db: Session,
    cardapio_id: int,
) -> Cardapio:
    return verificar_cardapio(db, cardapio_id)


def atualizar_cardapio(
    db: Session,
    cardapio_id: int,
    dados: CardapioUpdate,
) -> Cardapio:
    cardapio = verificar_cardapio(db, cardapio_id)

    campos = dados.model_dump(exclude_unset=True)

    if "nome" in campos and campos["nome"] is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="O nome do cardápio não pode ser nulo.",
        )

    dados_atualizacao = CardapioUpdate(**campos)

    return repository.atualizar_cardapio(
        db,
        cardapio,
        dados_atualizacao,
    )


def alterar_status_cardapio(
    db: Session,
    cardapio_id: int,
    ativo: bool,
) -> Cardapio:
    cardapio = verificar_cardapio(db, cardapio_id)

    if ativo:
        verificar_loja(db, cardapio.loja_id)

    return repository.alterar_status_cardapio(
        db,
        cardapio,
        ativo,
    )


#Produtos

def adicionar_produto(
    db: Session,
    cardapio_id: int,
    dados: CardapioProdutoCreate,
) -> CardapioProduto:
    cardapio = verificar_cardapio(db, cardapio_id)

    if not cardapio.ativo:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não é possível alterar um cardápio inativo.",
        )

    verificar_loja(db, cardapio.loja_id)

    verificar_produto(
        db,
        dados.produto_id,
        cardapio.loja_id,
    )

    item_existente = repository.buscar_item_cardapio(
        db,
        cardapio_id,
        dados.produto_id,
    )

    if item_existente is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Este produto já está associado ao cardápio.",
        )

    return repository.adicionar_produto(
        db,
        cardapio_id,
        dados,
    )


def listar_produtos_cardapio(
    db: Session,
    cardapio_id: int,
    incluir_indisponiveis: bool = False,
) -> list[CardapioProduto]:
    verificar_cardapio(db, cardapio_id)

    return repository.listar_produtos_cardapio(
        db,
        cardapio_id,
        incluir_indisponiveis,
    )


def atualizar_item_cardapio(
    db: Session,
    cardapio_id: int,
    produto_id: int,
    dados: CardapioProdutoUpdate,
) -> CardapioProduto:
    cardapio = verificar_cardapio(db, cardapio_id)

    if not cardapio.ativo:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não é possível alterar um cardápio inativo.",
        )

    item = repository.buscar_item_cardapio(
        db,
        cardapio_id,
        produto_id,
    )

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado neste cardápio.",
        )

    campos = dados.model_dump(exclude_unset=True)

    if not campos:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Informe ao menos um campo para atualizar.",
        )

    if "preco" in campos and campos["preco"] is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="O preço do cardápio não pode ser nulo.",
        )

    dados_atualizacao = CardapioProdutoUpdate(**campos)

    return repository.atualizar_item_cardapio(
        db,
        item,
        dados_atualizacao,
    )


def remover_produto_cardapio(
    db: Session,
    cardapio_id: int,
    produto_id: int,
) -> None:
    cardapio = verificar_cardapio(db, cardapio_id)

    if not cardapio.ativo:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não é possível alterar um cardápio inativo.",
        )

    item = repository.buscar_item_cardapio(
        db,
        cardapio_id,
        produto_id,
    )

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado neste cardápio.",
        )

    repository.remover_item_cardapio(db, item)
