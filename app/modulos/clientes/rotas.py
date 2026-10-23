
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.modulos.clientes import service
from app.modulos.clientes.schema import (
    ClienteCreate,
    ClienteResponse,
    ClienteUpdate,
)


router = APIRouter(
    prefix="/clientes",
    tags=["Clientes"],
)


@router.post(
    "/",
    response_model=ClienteResponse,
    status_code=status.HTTP_201_CREATED,
)
def criar_cliente(
    dados: ClienteCreate,
    db: Session = Depends(get_db),
):
    dados_cliente = dados.model_dump()

    return service.criar_cliente(
        db=db,
        dados=dados_cliente,
    )


@router.get(
    "/",
    response_model=list[ClienteResponse],
)
def listar_clientes(
    db: Session = Depends(get_db),
):
    return service.listar_clientes(db)


@router.get(
    "/{cliente_id}",
    response_model=ClienteResponse,
)
def buscar_cliente(
    cliente_id: int,
    db: Session = Depends(get_db),
):
    return service.buscar_cliente_por_id(
        db=db,
        cliente_id=cliente_id,
    )


@router.patch(
    "/{cliente_id}",
    response_model=ClienteResponse,
)
def atualizar_cliente(
    cliente_id: int,
    dados: ClienteUpdate,
    db: Session = Depends(get_db),
):
    dados_cliente = dados.model_dump(exclude_unset=True)

    return service.atualizar_cliente(
        db=db,
        cliente_id=cliente_id,
        dados=dados_cliente,
    )


@router.delete(
    "/{cliente_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def excluir_cliente(
    cliente_id: int,
    db: Session = Depends(get_db),
):
    service.excluir_cliente(
        db=db,
        cliente_id=cliente_id,
    )
