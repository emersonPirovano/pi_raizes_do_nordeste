
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.modulos.produtos import service
from app.modulos.produtos.schema import (
    ProdutoCreate,
    ProdutoResponse,
    ProdutoStatusUpdate,
    ProdutoUpdate,
)


router = APIRouter(
    prefix="/produtos",
    tags=["Produtos"],
)


@router.post(
    "/",
    response_model=ProdutoResponse,
    status_code=status.HTTP_201_CREATED,
)
def criar_produto(
    dados: ProdutoCreate,
    db: Session = Depends(get_db),
):
    return service.criar_produto(db, dados)


@router.get(
    "/",
    response_model=list[ProdutoResponse],
)
def listar_produtos(
    loja_id: int | None = Query(default=None, gt=0),
    incluir_inativos: bool = False,
    db: Session = Depends(get_db),
):
    return service.listar_produtos(
        db=db,
        loja_id=loja_id,
        incluir_inativos=incluir_inativos,
    )


@router.get(
    "/{produto_id}",
    response_model=ProdutoResponse,
)
def buscar_produto(
    produto_id: int,
    db: Session = Depends(get_db),
):
    return service.buscar_produto(db, produto_id)


@router.put(
    "/{produto_id}",
    response_model=ProdutoResponse,
)
def atualizar_produto(
    produto_id: int,
    dados: ProdutoUpdate,
    db: Session = Depends(get_db),
):
    return service.atualizar_produto(
        db=db,
        produto_id=produto_id,
        dados=dados,
    )


@router.patch(
    "/{produto_id}/status",
    response_model=ProdutoResponse,
)
def alterar_status_produto(
    produto_id: int,
    dados: ProdutoStatusUpdate,
    db: Session = Depends(get_db),
):
    return service.alterar_status_produto(
        db=db,
        produto_id=produto_id,
        ativo=dados.ativo,
    )
