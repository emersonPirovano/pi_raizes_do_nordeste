
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.modulos.estoque import service
from app.modulos.estoque.schema import (
    EstoqueCreate,
    EstoqueResponse,
    EstoqueUpdate,
)


router = APIRouter(
    prefix="/estoque",
    tags=["Estoque"],
)


@router.post(
    "/",
    response_model=EstoqueResponse,
    status_code=status.HTTP_201_CREATED,
)
def criar_estoque(
    dados: EstoqueCreate,
    db: Session = Depends(get_db),
):
    return service.criar_estoque(
        db=db,
        loja_id=dados.loja_id,
        produto_id=dados.produto_id,
        quantidade=dados.quantidade,
        quantidade_minima=dados.quantidade_minima,
    )


@router.get(
    "/",
    response_model=list[EstoqueResponse],
)
def listar_estoques(
    loja_id: int | None = Query(default=None, gt=0),
    produto_id: int | None = Query(default=None, gt=0),
    apenas_baixo: bool = Query(default=False),
    db: Session = Depends(get_db),
):
    return service.listar_estoques(
        db=db,
        loja_id=loja_id,
        produto_id=produto_id,
        apenas_baixo=apenas_baixo,
    )


@router.get(
    "/{estoque_id}",
    response_model=EstoqueResponse,
)
def buscar_estoque(
    estoque_id: int,
    db: Session = Depends(get_db),
):
    return service.buscar_estoque_por_id(
        db=db,
        estoque_id=estoque_id,
    )


@router.patch(
    "/{estoque_id}",
    response_model=EstoqueResponse,
)
def atualizar_estoque(
    estoque_id: int,
    dados: EstoqueUpdate,
    db: Session = Depends(get_db),
):
    return service.atualizar_estoque(
        db=db,
        estoque_id=estoque_id,
        quantidade=dados.quantidade,
        quantidade_minima=dados.quantidade_minima,
    )


@router.delete(
    "/{estoque_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def excluir_estoque(
    estoque_id: int,
    db: Session = Depends(get_db),
):
    service.excluir_estoque(
        db=db,
        estoque_id=estoque_id,
    )
