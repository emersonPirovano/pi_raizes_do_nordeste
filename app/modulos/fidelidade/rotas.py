
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.modulos.fidelidade import service
from app.modulos.fidelidade.schema import (
    FidelidadeCreate,
    FidelidadeResponse,
    ResgatePontosCreate,
    MovimentacaoPontosResponse,
    SaldoPontosResponse,
)

router = APIRouter(
    prefix="/fidelidade",
    tags=["Fidelidade"]
)


@router.post(
    "/",
    response_model=FidelidadeResponse,
    status_code=status.HTTP_201_CREATED
)
def criar_fidelidade(
    dados: FidelidadeCreate,
    db: Session = Depends(get_db)
):
    return service.criar_fidelidade(db, dados.cliente_id)


@router.get(
    "/",
    response_model=list[FidelidadeResponse]
)
def listar_fidelidades(
    db: Session = Depends(get_db)
):
    return service.listar_fidelidades(db)


@router.get(
    "/cliente/{cliente_id}/saldo",
    response_model=SaldoPontosResponse
)
def consultar_saldo(
    cliente_id: int,
    db: Session = Depends(get_db)
):
    return service.consultar_saldo(db, cliente_id)


@router.post(
    "/pedido/{pedido_id}/creditar",
    response_model=MovimentacaoPontosResponse
)
def creditar_pontos(
    pedido_id: int,
    db: Session = Depends(get_db)
):
    return service.creditar_pontos_por_pedido(db, pedido_id)


@router.post(
    "/cliente/{cliente_id}/resgatar",
    response_model=MovimentacaoPontosResponse
)
def resgatar_pontos(
    cliente_id: int,
    dados: ResgatePontosCreate,
    db: Session = Depends(get_db)
):
    return service.resgatar_pontos(
        db,
        cliente_id,
        dados.quantidade_pontos,
        dados.descricao
    )


@router.get(
    "/cliente/{cliente_id}/movimentacoes",
    response_model=list[MovimentacaoPontosResponse]
)
def listar_movimentacoes(
    cliente_id: int,
    db: Session = Depends(get_db)
):
    return service.listar_movimentacoes(db, cliente_id)
