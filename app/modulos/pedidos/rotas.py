
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.modulos.pedidos import service
from app.modulos.pedidos.schema import (
    PedidoCreate,
    PedidoUpdate,
    PedidoResponse,
    ItemPedidoCreate,
    ItemPedidoUpdate,
    ItemPedidoResponse,
)

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])


#pedidos

@router.post(
    "/",
    response_model=PedidoResponse,
    status_code=status.HTTP_201_CREATED
)
def criar_pedido(
    dados: PedidoCreate,
    db: Session = Depends(get_db)
):
    return service.criar_pedido(db, dados.model_dump())


@router.get("/", response_model=list[PedidoResponse])
def listar_pedidos(
    cliente_id: int | None = Query(None, gt=0),
    loja_id: int | None = Query(None, gt=0),
    db: Session = Depends(get_db)
):
    return service.listar_pedidos(
        db,
        cliente_id=cliente_id,
        loja_id=loja_id
    )


@router.get("/{pedido_id}", response_model=PedidoResponse)
def buscar_pedido(
    pedido_id: int,
    db: Session = Depends(get_db)
):
    return service.buscar_pedido_por_id(db, pedido_id)


@router.patch("/{pedido_id}", response_model=PedidoResponse)
def atualizar_pedido(
    pedido_id: int,
    dados: PedidoUpdate,
    db: Session = Depends(get_db)
):
    return service.atualizar_pedido(
        db,
        pedido_id,
        dados.model_dump(exclude_unset=True)
    )


@router.delete(
    "/{pedido_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def excluir_pedido(
    pedido_id: int,
    db: Session = Depends(get_db)
):
    service.excluir_pedido(db, pedido_id)
    return None


#itens do pedido

@router.post(
    "/{pedido_id}/itens",
    response_model=ItemPedidoResponse,
    status_code=status.HTTP_201_CREATED
)
def adicionar_item(
    pedido_id: int,
    dados: ItemPedidoCreate,
    db: Session = Depends(get_db)
):
    return service.adicionar_item_pedido(
        db,
        pedido_id,
        dados.model_dump()
    )


@router.get(
    "/{pedido_id}/itens",
    response_model=list[ItemPedidoResponse]
)
def listar_itens(
    pedido_id: int,
    db: Session = Depends(get_db)
):
    service.buscar_pedido_por_id(db, pedido_id)
    return service.listar_itens_pedido(db, pedido_id)


@router.patch(
    "/{pedido_id}/itens/{produto_id}",
    response_model=ItemPedidoResponse
)
def atualizar_item(
    pedido_id: int,
    produto_id: int,
    dados: ItemPedidoUpdate,
    db: Session = Depends(get_db)
):
    return service.atualizar_item_pedido(
        db,
        pedido_id,
        produto_id,
        dados.quantidade
    )


@router.delete(
    "/{pedido_id}/itens/{produto_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def remover_item(
    pedido_id: int,
    produto_id: int,
    db: Session = Depends(get_db)
):
    service.remover_item_pedido(
        db,
        pedido_id,
        produto_id
    )
    return None
