
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from api import (
    app,
    obter_sessao,
    popular_se_vazio,
    ServicoCatalogo,
    RepositorioProdutos,
)
from loja.banco import engine_em_memoria, criar_tabelas


cliente = TestClient(app)


@pytest.fixture(autouse=True)
def banco_de_teste():
    """Cada teste ganha um banco novo, na memória, com os 3 produtos."""
    engine = engine_em_memoria()
    criar_tabelas(engine)

    with Session(engine) as sessao:
        popular_se_vazio(
            ServicoCatalogo(RepositorioProdutos(sessao))
        )

    def sessao_de_teste():
        with Session(engine) as sessao:
            yield sessao

    app.dependency_overrides[obter_sessao] = sessao_de_teste
    cliente.delete("/carrinho")

    yield

    app.dependency_overrides.clear()
    engine.dispose()


def test_vitrine_tem_tres_produtos():
    resposta = cliente.get("/produtos")

    assert resposta.status_code == 200
    assert len(resposta.json()) == 3


def test_produto_inexistente_da_404():
    resposta = cliente.get("/produtos/99")

    assert resposta.status_code == 404


def test_filtro_por_tamanho():
    resposta = cliente.get(
        "/produtos",
        params={"tamanho": "M"},
    )
    nomes = [p["nome"] for p in resposta.json()]

    assert nomes == ["Camiseta básica"]


def test_quantidade_zero_da_422():
    resposta = cliente.post(
        "/carrinho/itens",
        json={"produto_id": 1, "quantidade": 0},
    )

    assert resposta.status_code == 422


def test_adicionar_item_da_201():
    resposta = cliente.post(
        "/carrinho/itens",
        json={"produto_id": 1, "quantidade": 2},
    )

    assert resposta.status_code == 201
    assert resposta.json()["pecas_no_carrinho"] == 2


def test_total_com_promocao_sem_frete():
    cliente.post(
        "/carrinho/itens",
        json={"produto_id": 1, "quantidade": 3},
    )
    cliente.post(
        "/carrinho/itens",
        json={"produto_id": 2, "quantidade": 1},
    )

    resposta = cliente.get("/carrinho/total")

    assert resposta.json()["pecas"] == 4
    assert resposta.json()["subtotal"] == 249.6
    assert resposta.json()["total"] == 224.64


def test_total_abaixo_de_200_paga_frete():
    cliente.post(
        "/carrinho/itens",
        json={"produto_id": 1, "quantidade": 1},
    )

    resposta = cliente.get("/carrinho/total")

    assert resposta.json()["total"] == 50.91


def test_cadastrar_produto():
    resposta = cliente.post(
        "/produtos",
        json={
            "nome": "Boné",
            "preco": 49.9,
            "tamanho": "M",
        },
    )

    assert resposta.status_code == 201
    assert resposta.json()["nome"] == "Boné"


def test_produto_duplicado_da_409():
    dados = {
        "nome": "Boné",
        "preco": 49.9,
        "tamanho": "M",
    }

    cliente.post("/produtos", json=dados)
    resposta = cliente.post("/produtos", json=dados)

    assert resposta.status_code == 409


def test_dados_invalidos_dao_422():
    resposta = cliente.post(
        "/produtos",
        json={
            "nome": "Camiseta inválida",
            "preco": -10,
            "tamanho": "M",
        },
    )

    assert resposta.status_code == 422


def test_atualizar_produto():
    resposta = cliente.put(
        "/produtos/1",
        json={
            "nome": "Camiseta atualizada",
            "preco": 45.9,
            "tamanho": "M",
            "tipo": "Camiseta",
            "manga": "curta",
        },
    )

    assert resposta.status_code == 200
    assert resposta.json()["nome"] == "Camiseta atualizada"


def test_remover_produto():
    resposta = cliente.delete("/produtos/1")

    assert resposta.status_code == 204
    assert cliente.get("/produtos/1").status_code == 404
