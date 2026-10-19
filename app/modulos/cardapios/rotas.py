
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.modulos.cardapios import service
from app.modulos.cardapios.schema import (
    CardapioCreate,
    CardapioResponse,
    CardapioStatusUpdate,
    CardapioUpdate,
    CardapioProdutoCreate,
    CardapioProdutoResponse,
    CardapioProdutoUpdate,
)


router = APIRouter(
    prefix="/cardapios",
    tags=["Cardápios"],
)


#Cardápio

@router.post(
    "/",
    response_model=CardapioResponse,
    status_code=status.HTTP_201_CREATED,
)
def criar_cardapio(
    dados: CardapioCreate,
    db: Session = Depends(get_db),
):
    return service.criar_cardapio(db, dados)


@router.get(
    "/",
    response_model=list[CardapioResponse],
)
def listar_cardapios(
    incluir_inativos: bool = False,
    db: Session = Depends(get_db),
):
    return service.listar_cardapios(
        db=db,
        incluir_inativos=incluir_inativos,
    )


@router.get(
    "/{cardapio_id}",
    response_model=CardapioResponse,
)
def buscar_cardapio(
    cardapio_id: int,
    db: Session = Depends(get_db),
):
    return service.buscar_cardapio(db, cardapio_id)


@router.put(
    "/{cardapio_id}",
    response_model=CardapioResponse,
)
def atualizar_cardapio(
    cardapio_id: int,
    dados: CardapioUpdate,
    db: Session = Depends(get_db),
):
    return service.atualizar_cardapio(
        db=db,
        cardapio_id=cardapio_id,
        dados=dados,
    )


@router.patch(
    "/{cardapio_id}/status",
    response_model=CardapioResponse,
)
def alterar_status_cardapio(
    cardapio_id: int,
    dados: CardapioStatusUpdate,
    db: Session = Depends(get_db),
):
    return service.alterar_status_cardapio(
        db=db,
        cardapio_id=cardapio_id,
        ativo=dados.ativo,
    )


#Produtos

@router.post(
    "/{cardapio_id}/produtos",
    response_model=CardapioProdutoResponse,
    status_code=status.HTTP_201_CREATED,
)
def adicionar_produto(
    cardapio_id: int,
    dados: CardapioProdutoCreate,
    db: Session = Depends(get_db),
):
    return service.adicionar_produto(
        db=db,
        cardapio_id=cardapio_id,
        dados=dados,
    )


@router.get(
    "/{cardapio_id}/produtos",
    response_model=list[CardapioProdutoResponse],
)
def listar_produtos_cardapio(
    cardapio_id: int,
    incluir_indisponiveis: bool = False,
    db: Session = Depends(get_db),
):
    return service.listar_produtos_cardapio(
        db=db,
        cardapio_id=cardapio_id,
        incluir_indisponiveis=incluir_indisponiveis,
    )


@router.patch(
    "/{cardapio_id}/produtos/{produto_id}",
    response_model=CardapioProdutoResponse,
)
def atualizar_item_cardapio(
    cardapio_id: int,
    produto_id: int,
    dados: CardapioProdutoUpdate,
    db: Session = Depends(get_db),
):
    return service.atualizar_item_cardapio(
        db=db,
        cardapio_id=cardapio_id,
        produto_id=produto_id,
        dados=dados,
    )


@router.delete(
    "/{cardapio_id}/produtos/{produto_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remover_produto_cardapio(
    cardapio_id: int,
    produto_id: int,
    db: Session = Depends(get_db),
):
    service.remover_produto_cardapio(
        db=db,
        cardapio_id=cardapio_id,
        produto_id=produto_id,
    )
