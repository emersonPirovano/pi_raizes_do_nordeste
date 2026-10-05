from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.modulos.lojas import service
from app.modulos.lojas.schema import (
    LojaCreate,
    LojaUpdate,
    LojaResponse,
)

router = APIRouter(
    prefix="/lojas",
    tags=["Lojas"]
)


@router.post(
    "/",
    response_model=LojaResponse,
    status_code=status.HTTP_201_CREATED
)
def criar_loja(
    dados: LojaCreate,
    db: Session = Depends(get_db)
):
    return service.criar_loja(
        db,
        dados.model_dump()
    )


@router.get(
    "/",
    response_model=list[LojaResponse]
)
def listar_lojas(
    db: Session = Depends(get_db)
):
    return service.listar_lojas(db)


@router.get(
    "/{loja_id}",
    response_model=LojaResponse
)
def buscar_loja(
    loja_id: int,
    db: Session = Depends(get_db)
):
    return service.buscar_loja(db, loja_id)


@router.put(
    "/{loja_id}",
    response_model=LojaResponse
)
def atualizar_loja(
    loja_id: int,
    dados: LojaUpdate,
    db: Session = Depends(get_db)
):
    return service.atualizar_loja(
        db,
        loja_id,
        dados.model_dump(exclude_unset=True)
    )


@router.patch(
    "/{loja_id}/status",
    response_model=LojaResponse
)
def alterar_status(
    loja_id: int,
    ativa: bool,
    db: Session = Depends(get_db)
):
    return service.alterar_status(
        db,
        loja_id,
        ativa
    )