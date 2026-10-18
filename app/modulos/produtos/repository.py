
from sqlalchemy.orm import Session

from app.modulos.produtos.model_db import Produto
from app.modulos.produtos.schema import ProdutoCreate, ProdutoUpdate


def criar_produto(
    db: Session,
    dados: ProdutoCreate,
) -> Produto:
    produto = Produto(**dados.model_dump())

    db.add(produto)
    db.commit()
    db.refresh(produto)

    return produto


def listar_produtos(
    db: Session,
    loja_id: int | None = None,
    incluir_inativos: bool = False,
) -> list[Produto]:
    consulta = db.query(Produto)

    if loja_id is not None:
        consulta = consulta.filter(Produto.loja_id == loja_id)

    if not incluir_inativos:
        consulta = consulta.filter(Produto.ativo.is_(True))

    return consulta.order_by(Produto.nome.asc()).all()


def buscar_produto_por_id(
    db: Session,
    produto_id: int,
) -> Produto | None:
    return (
        db.query(Produto)
        .filter(Produto.id == produto_id)
        .first()
    )


def atualizar_produto(
    db: Session,
    produto: Produto,
    dados: ProdutoUpdate,
) -> Produto:
    campos = dados.model_dump(exclude_unset=True)

    for campo, valor in campos.items():
        setattr(produto, campo, valor)

    db.commit()
    db.refresh(produto)

    return produto


def alterar_status_produto(
    db: Session,
    produto: Produto,
    ativo: bool,
) -> Produto:
    produto.ativo = ativo

    db.commit()
    db.refresh(produto)

    return produto
