from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from loja.carrinho import Carrinho
from loja.promocao import Percentual
from loja.produto import Calca, Camiseta, Produto


app = FastAPI(title="Loja de Roupas")


class ItemPedido(BaseModel):
    produto_id: int
    quantidade: int = Field(gt=0, le=10)


CATALOGO = {
    1: Camiseta("Camiseta básica", 39.90, "M", "curta"),
    2: Calca("Calça jeans", 129.90, "G", "reta"),
    3: Produto("Moletom", 159.90, "P"),
}


def novo_carrinho():
    return Carrinho(Percentual(10))


carrinho = novo_carrinho()


def com_id(produto_id, produto):
    return {
        "id": produto_id,
        **produto.para_dict()
    }


@app.get("/")
def inicio():
    return {
        "loja": "Loja de Roupas",
        "documentacao": "/docs"
    }


@app.get("/produtos")
def listar_produtos(
    tamanho: str | None = None,
    preco_max: float | None = None
):
    resultado = []

    for produto_id, produto in CATALOGO.items():
        if tamanho is not None and produto.tamanho != tamanho:
            continue

        if preco_max is not None and produto.preco > preco_max:
            continue

        resultado.append(com_id(produto_id, produto))

    return resultado


@app.get("/produtos/{produto_id}")
def buscar_produto(produto_id: int):
    if produto_id not in CATALOGO:
        raise HTTPException(
            status_code=404,
            detail="produto não encontrado"
        )

    return com_id(produto_id, CATALOGO[produto_id])


@app.post("/carrinho/itens", status_code=201)
def adicionar_item(item: ItemPedido):
    if item.produto_id not in CATALOGO:
        raise HTTPException(
            status_code=404,
            detail="produto não encontrado"
        )

    produto = CATALOGO[item.produto_id]
    carrinho.adicionar(produto, item.quantidade)

    return {
        "adicionado": com_id(item.produto_id, produto),
        "quantidade": item.quantidade,
        "pecas_no_carrinho": carrinho.quantidade_de_pecas
    }


@app.get("/carrinho/total")
def total_do_carrinho():
    return {
        "pecas": carrinho.quantidade_de_pecas,
        "subtotal": round(carrinho.subtotal, 2),
        "total": round(carrinho.total, 2)
    }


@app.delete("/carrinho", status_code=204)
def esvaziar_carrinho():
    global carrinho
    carrinho = novo_carrinho()