
from contextlib import asynccontextmanager
from typing import Literal

from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from sqlmodel import Session

from loja.banco import criar_engine, criar_tabelas
from loja.carrinho import Carrinho
from loja.promocao import Percentual
from loja.repositorio import RepositorioProdutos
from loja.servico import (
    DadosInvalidos,
    ProdutoJaExiste,
    ProdutoNaoEncontrado,
    ServicoCatalogo,
    com_id,
)


class ProdutoEntrada(BaseModel):
    tipo: Literal["Produto", "Camiseta", "Calca"] = "Produto"
    nome: str
    preco: float
    tamanho: str
    manga: str | None = None
    modelagem: str | None = None


class ItemPedido(BaseModel):
    produto_id: int
    quantidade: int = Field(gt=0, le=10)


engine = criar_engine()

CATALOGO_INICIAL = [
    {
        "tipo": "Camiseta",
        "nome": "Camiseta básica",
        "preco": 39.90,
        "tamanho": "M",
        "manga": "curta",
    },
    {
        "tipo": "Calca",
        "nome": "Calça jeans",
        "preco": 129.90,
        "tamanho": "G",
        "modelagem": "reta",
    },
    {
        "tipo": "Produto",
        "nome": "Moletom",
        "preco": 159.90,
        "tamanho": "P",
    },
]


def popular_se_vazio(servico):
    if not servico.listar():
        for dados in CATALOGO_INICIAL:
            servico.cadastrar(dados)


@asynccontextmanager
async def ciclo_de_vida(app):
    criar_tabelas(engine)

    with Session(engine) as sessao:
        popular_se_vazio(
            ServicoCatalogo(RepositorioProdutos(sessao))
        )

    yield


app = FastAPI(
    title="Loja de Roupas",
    lifespan=ciclo_de_vida,
)


def obter_sessao():
    with Session(engine) as sessao:
        yield sessao


def obter_servico(sessao: Session = Depends(obter_sessao)):
    return ServicoCatalogo(RepositorioProdutos(sessao))


@app.exception_handler(ProdutoNaoEncontrado)
def nao_encontrado(request, erro):
    return JSONResponse(
        status_code=404,
        content={"detail": str(erro)},
    )


@app.exception_handler(ProdutoJaExiste)
def ja_existe(request, erro):
    return JSONResponse(
        status_code=409,
        content={"detail": str(erro)},
    )


@app.exception_handler(DadosInvalidos)
def dados_invalidos(request, erro):
    return JSONResponse(
        status_code=422,
        content={"detail": str(erro)},
    )


def novo_carrinho():
    return Carrinho(Percentual(10))


carrinho = novo_carrinho()


@app.get("/")
def inicio():
    return {
        "loja": "Loja de Roupas",
        "documentacao": "/docs",
    }


@app.get("/produtos")
def listar_produtos(
    tamanho: str | None = None,
    preco_max: float | None = None,
    servico=Depends(obter_servico),
):
    return servico.listar(tamanho, preco_max)


@app.get("/produtos/{produto_id}")
def buscar_produto(
    produto_id: int,
    servico=Depends(obter_servico),
):
    return servico.buscar(produto_id)


@app.post("/produtos", status_code=201)
def cadastrar_produto(
    dados: ProdutoEntrada,
    servico=Depends(obter_servico),
):
    return servico.cadastrar(dados.model_dump())


@app.put("/produtos/{produto_id}")
def atualizar_produto(
    produto_id: int,
    dados: ProdutoEntrada,
    servico=Depends(obter_servico),
):
    return servico.atualizar(produto_id, dados.model_dump())


@app.delete("/produtos/{produto_id}", status_code=204)
def remover_produto(
    produto_id: int,
    servico=Depends(obter_servico),
):
    servico.remover(produto_id)


@app.post("/carrinho/itens", status_code=201)
def adicionar_item(
    item: ItemPedido,
    servico=Depends(obter_servico),
):
    produto = servico.produto(item.produto_id)
    carrinho.adicionar(produto, item.quantidade)

    return {
        "adicionado": com_id(item.produto_id, produto),
        "quantidade": item.quantidade,
        "pecas_no_carrinho": carrinho.quantidade_de_pecas,
    }


@app.get("/carrinho/total")
def total_do_carrinho():
    return {
        "pecas": carrinho.quantidade_de_pecas,
        "subtotal": round(carrinho.subtotal, 2),
        "total": round(carrinho.total, 2),
    }


@app.delete("/carrinho", status_code=204)
def esvaziar_carrinho():
    global carrinho
    carrinho = novo_carrinho()
