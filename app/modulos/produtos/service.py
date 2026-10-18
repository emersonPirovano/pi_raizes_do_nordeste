
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.modulos.lojas.model_db import Loja
from app.modulos.produtos import repository
from app.modulos.produtos.model_db import Produto
from app.modulos.produtos.schema import ProdutoCreate, ProdutoUpdate


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
            detail="Não é possível operar com uma loja inativa.",
        )

    return loja


def verificar_codigo_duplicado(
    db: Session,
    loja_id: int,
    codigo: str | None,
    produto_id: int | None = None,
) -> None:
    if codigo is None:
        return

    codigo = codigo.strip()

    if not codigo:
        return

    consulta = db.query(Produto).filter(
        Produto.loja_id == loja_id,
        Produto.codigo == codigo,
    )

    if produto_id is not None:
        consulta = consulta.filter(Produto.id != produto_id)

    if consulta.first() is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Já existe um produto com este código nesta loja.",
        )


def criar_produto(
    db: Session,
    dados: ProdutoCreate,
) -> Produto:
    verificar_loja(db, dados.loja_id)

    dados_produto = dados.model_dump()

    codigo = dados_produto.get("codigo")

    if codigo is not None:
        codigo = codigo.strip() or None
        dados_produto["codigo"] = codigo

    verificar_codigo_duplicado(
        db=db,
        loja_id=dados.loja_id,
        codigo=codigo,
    )

    dados_validados = ProdutoCreate(**dados_produto)

    return repository.criar_produto(db, dados_validados)


def listar_produtos(
    db: Session,
    loja_id: int | None = None,
    incluir_inativos: bool = False,
) -> list[Produto]:
    if loja_id is not None:
        verificar_loja(db, loja_id)

    return repository.listar_produtos(
        db=db,
        loja_id=loja_id,
        incluir_inativos=incluir_inativos,
    )


def buscar_produto(
    db: Session,
    produto_id: int,
) -> Produto:
    produto = repository.buscar_produto_por_id(
        db,
        produto_id,
    )

    if produto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado.",
        )

    return produto


def atualizar_produto(
    db: Session,
    produto_id: int,
    dados: ProdutoUpdate,
) -> Produto:
    produto = buscar_produto(db, produto_id)

    campos = dados.model_dump(exclude_unset=True)

    if "nome" in campos and campos["nome"] is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="O nome do produto não pode ser nulo.",
        )

    if "preco" in campos and campos["preco"] is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="O preço do produto não pode ser nulo.",
        )

    if "codigo" in campos and campos["codigo"] is not None:
        codigo = campos["codigo"].strip()
        campos["codigo"] = codigo or None

    verificar_codigo_duplicado(
        db=db,
        loja_id=produto.loja_id,
        codigo=campos.get("codigo", produto.codigo),
        produto_id=produto.id,
    )

    dados_atualizacao = ProdutoUpdate(**campos)

    return repository.atualizar_produto(
        db,
        produto,
        dados_atualizacao,
    )


def alterar_status_produto(
    db: Session,
    produto_id: int,
    ativo: bool,
) -> Produto:
    produto = buscar_produto(db, produto_id)

    if ativo:
        verificar_loja(db, produto.loja_id)

    return repository.alterar_status_produto(
        db,
        produto,
        ativo,
    )
