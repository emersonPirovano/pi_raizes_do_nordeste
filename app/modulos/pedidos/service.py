
from decimal import Decimal, ROUND_HALF_UP

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.modulos.pedidos import repository
from app.modulos.clientes.model_db import Cliente
from app.modulos.lojas.model_db import Loja
from app.modulos.produtos.model_db import Produto
from app.modulos.pedidos.model_db import Pedido
from app.modulos.cardapios.model_db import Cardapio, CardapioProduto


def calcular_valor(valor: Decimal) -> Decimal:
    return valor.quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )


def validar_cliente_e_loja(
    db: Session,
    cliente_id: int,
    loja_id: int,
) -> None:
    cliente = db.get(Cliente, cliente_id)

    if cliente is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não encontrado.",
        )

    loja = db.get(Loja, loja_id)

    if loja is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Loja não encontrada.",
        )

    if not loja.ativa:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não é possível realizar pedidos para uma loja inativa.",
        )


def validar_produto(
    db: Session,
    produto_id: int,
    loja_id: int,
) -> CardapioProduto:

    produto = db.get(Produto, produto_id)

    if produto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado.",
        )

    if produto.loja_id != loja_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Produto não pertence à loja informada.",
        )

    if not produto.ativo:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O produto está inativo.",
        )

    cardapio = db.query(Cardapio).filter(
        Cardapio.loja_id == loja_id
    ).first()

    if cardapio is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cardápio da loja não encontrado.",
        )

    if not cardapio.ativo:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O cardápio da loja está inativo.",
        )

    item_cardapio = db.query(CardapioProduto).filter(
        CardapioProduto.cardapio_id == cardapio.id,
        CardapioProduto.produto_id == produto_id,
    ).first()

    if item_cardapio is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Produto não cadastrado no cardápio.",
        )

    if not item_cardapio.disponivel:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Produto indisponível no cardápio.",
        )

    return item_cardapio


def validar_pedido_pendente(pedido: Pedido) -> None:
    if pedido.status != "PENDENTE":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Somente pedidos pendentes podem ser modificados.",
        )


def recalcular_total(
    db: Session,
    pedido: Pedido,
) -> Decimal:
    itens = repository.listar_itens(db, pedido.id)

    valor_total = sum(
        (item.subtotal for item in itens),
        Decimal("0.00"),
    )

    valor_total = calcular_valor(valor_total)

    repository.atualizar_valor_total(
        db,
        pedido,
        valor_total,
    )

    return valor_total


# criar pedido

def criar_pedido(
    db: Session,
    dados: dict,
):
    validar_cliente_e_loja(
        db,
        dados["cliente_id"],
        dados["loja_id"],
    )

    produtos = []
    produtos_ids = set()
    valor_total = Decimal("0.00")

    for item in dados["itens"]:
        produto_id = item["produto_id"]

        if produto_id in produtos_ids:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Não repita o mesmo produto no pedido. Informe a quantidade total em um único item.",
            )

        produtos_ids.add(produto_id)

        item_cardapio = validar_produto(
            db,
            produto_id,
            dados["loja_id"],
        )

        preco_unitario = calcular_valor(
            Decimal(str(item_cardapio.preco))
        )

        quantidade = item["quantidade"]

        subtotal = calcular_valor(
            preco_unitario * quantidade
        )

        valor_total += subtotal

        produtos.append({
            "produto_id": produto_id,
            "quantidade": quantidade,
            "preco_unitario": preco_unitario,
            "subtotal": subtotal,
        })

    try:
        pedido = repository.criar_pedido(
            db=db,
            cliente_id=dados["cliente_id"],
            loja_id=dados["loja_id"],
            valor_total=calcular_valor(valor_total),
        )

        for item in produtos:
            repository.adicionar_item(
                db=db,
                pedido_id=pedido.id,
                produto_id=item["produto_id"],
                quantidade=item["quantidade"],
                preco_unitario=item["preco_unitario"],
                subtotal=item["subtotal"],
            )

        db.commit()
        db.refresh(pedido)

        return pedido

    except Exception:
        db.rollback()
        raise


# listar pedidos

def listar_pedidos(
    db: Session,
    cliente_id: int | None = None,
    loja_id: int | None = None,
):
    return repository.listar_pedidos(
        db,
        cliente_id=cliente_id,
        loja_id=loja_id,
    )


# buscar pedidos

def buscar_pedido_por_id(
    db: Session,
    pedido_id: int,
):
    pedido = repository.buscar_pedido_por_id(
        db,
        pedido_id,
    )

    if pedido is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pedido não encontrado.",
        )

    return pedido


# atualizar status

def atualizar_pedido(
    db: Session,
    pedido_id: int,
    dados: dict,
):
    pedido = buscar_pedido_por_id(db, pedido_id)

    validar_pedido_pendente(pedido)

    if "status" in dados:
        if dados["status"] is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="O status não pode ser nulo.",
            )

        status_permitidos = {
            "PENDENTE",
            "CONFIRMADO",
            "EM_PREPARACAO",
            "PRONTO",
            "CONCLUIDO",
            "CANCELADO",
        }

        novo_status = dados["status"].upper()

        if novo_status not in status_permitidos:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Status de pedido inválido.",
            )

        dados["status"] = novo_status

    return repository.atualizar_pedido(
        db,
        pedido,
        dados,
    )


# adicionar item

def adicionar_item_pedido(
    db: Session,
    pedido_id: int,
    dados: dict,
):
    pedido = buscar_pedido_por_id(db, pedido_id)

    validar_pedido_pendente(pedido)

    produto_id = dados["produto_id"]
    quantidade = dados["quantidade"]

    item_existente = repository.buscar_item(
        db,
        pedido_id,
        produto_id,
    )

    if item_existente is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Produto já existe neste pedido. Altere a quantidade do item existente.",
        )

    try:
        item_cardapio = validar_produto(
            db,
            produto_id,
            pedido.loja_id,
        )

        preco_unitario = calcular_valor(
            Decimal(str(item_cardapio.preco))
        )

        subtotal = calcular_valor(
            preco_unitario * quantidade
        )

        item = repository.adicionar_item(
            db=db,
            pedido_id=pedido.id,
            produto_id=produto_id,
            quantidade=quantidade,
            preco_unitario=preco_unitario,
            subtotal=subtotal,
        )

        pedido.valor_total = calcular_valor(
            pedido.valor_total + subtotal
        )

        db.commit()
        db.refresh(item)

        return item

    except Exception:
        db.rollback()
        raise


# alterar a quatidade

def atualizar_item_pedido(
    db: Session,
    pedido_id: int,
    produto_id: int,
    quantidade: int,
):
    pedido = buscar_pedido_por_id(db, pedido_id)

    validar_pedido_pendente(pedido)

    item = repository.buscar_item(
        db,
        pedido_id,
        produto_id,
    )

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item não encontrado neste pedido.",
        )

    try:
        subtotal = calcular_valor(
            item.preco_unitario * quantidade
        )

        repository.atualizar_item(
            db,
            item,
            quantidade,
            subtotal,
        )

        recalcular_total(db, pedido)

        db.commit()
        db.refresh(item)

        return item

    except Exception:
        db.rollback()
        raise


# remover item

def remover_item_pedido(
    db: Session,
    pedido_id: int,
    produto_id: int,
) -> None:
    pedido = buscar_pedido_por_id(db, pedido_id)

    validar_pedido_pendente(pedido)

    item = repository.buscar_item(
        db,
        pedido_id,
        produto_id,
    )

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item não encontrado neste pedido.",
        )

    try:
        repository.excluir_item(db, item)

        recalcular_total(db, pedido)

        db.commit()

    except Exception:
        db.rollback()
        raise


# excluir pedido

def excluir_pedido(
    db: Session,
    pedido_id: int,
) -> None:
    pedido = buscar_pedido_por_id(db, pedido_id)

    validar_pedido_pendente(pedido)

    try:
        repository.excluir_pedido(db, pedido)

    except Exception:
        db.rollback()
        raise
