
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modulos.pedidos.model_db import Pedido, ItemPedido


# pedido

def criar_pedido(
    db: Session,
    cliente_id: int,
    loja_id: int,
    valor_total: Decimal,
) -> Pedido:
    pedido = Pedido(
        cliente_id=cliente_id,
        loja_id=loja_id,
        valor_total=valor_total,
    )

    db.add(pedido)
    db.flush()

    return pedido


def listar_pedidos(
    db: Session,
    cliente_id: int | None = None,
    loja_id: int | None = None,
) -> list[Pedido]:
    consulta = select(Pedido)

    if cliente_id is not None:
        consulta = consulta.where(
            Pedido.cliente_id == cliente_id
        )

    if loja_id is not None:
        consulta = consulta.where(
            Pedido.loja_id == loja_id
        )

    consulta = consulta.order_by(Pedido.id.desc())

    return list(db.scalars(consulta).all())


def buscar_pedido_por_id(
    db: Session,
    pedido_id: int,
) -> Pedido | None:
    return db.get(Pedido, pedido_id)


def atualizar_pedido(
    db: Session,
    pedido: Pedido,
    dados: dict,
) -> Pedido:
    for campo, valor in dados.items():
        setattr(pedido, campo, valor)

    db.commit()
    db.refresh(pedido)

    return pedido


def excluir_pedido(
    db: Session,
    pedido: Pedido,
) -> None:
    db.delete(pedido)
    db.commit()


# itens do pedido

def adicionar_item(
    db: Session,
    pedido_id: int,
    produto_id: int,
    quantidade: int,
    preco_unitario: Decimal,
    subtotal: Decimal,
) -> ItemPedido:
    item = ItemPedido(
        pedido_id=pedido_id,
        produto_id=produto_id,
        quantidade=quantidade,
        preco_unitario=preco_unitario,
        subtotal=subtotal,
    )

    db.add(item)
    db.flush()

    return item


def listar_itens(
    db: Session,
    pedido_id: int,
) -> list[ItemPedido]:
    consulta = select(ItemPedido).where(
        ItemPedido.pedido_id == pedido_id
    )

    return list(db.scalars(consulta).all())


def buscar_item(
    db: Session,
    pedido_id: int,
    produto_id: int,
) -> ItemPedido | None:
    consulta = select(ItemPedido).where(
        ItemPedido.pedido_id == pedido_id,
        ItemPedido.produto_id == produto_id,
    )

    return db.scalars(consulta).first()


def atualizar_item(
    db: Session,
    item: ItemPedido,
    quantidade: int,
    subtotal: Decimal,
) -> ItemPedido:
    item.quantidade = quantidade
    item.subtotal = subtotal

    db.flush()

    return item


def excluir_item(
    db: Session,
    item: ItemPedido,
) -> None:
    db.delete(item)
    db.flush()


def atualizar_valor_total(
    db: Session,
    pedido: Pedido,
    valor_total: Decimal,
) -> Pedido:
    pedido.valor_total = valor_total

    db.flush()

    return pedido
