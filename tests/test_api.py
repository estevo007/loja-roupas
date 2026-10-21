import pytest
from fastapi.testclient import TestClient

from api import app


cliente = TestClient(app)


@pytest.fixture(autouse=True)
def carrinho_vazio():
    cliente.delete("/carrinho")


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
        params={"tamanho": "M"}
    )

    nomes = [p["nome"] for p in resposta.json()]

    assert nomes == ["Camiseta básica"]


def test_quantidade_zero_da_422():
    resposta = cliente.post(
        "/carrinho/itens",
        json={"produto_id": 1, "quantidade": 0}
    )

    assert resposta.status_code == 422


def test_adicionar_item_da_201():
    resposta = cliente.post(
        "/carrinho/itens",
        json={"produto_id": 1, "quantidade": 3}
    )

    assert resposta.status_code == 201
    assert resposta.json()["pecas_no_carrinho"] == 3


def test_total_com_promocao_sem_frete():
    cliente.post(
        "/carrinho/itens",
        json={"produto_id": 1, "quantidade": 3}
    )
    cliente.post(
        "/carrinho/itens",
        json={"produto_id": 2, "quantidade": 1}
    )

    resposta = cliente.get("/carrinho/total")

    assert resposta.json() == {
        "pecas": 4,
        "subtotal": 249.6,
        "total": 224.64
    }


def test_total_abaixo_de_200_paga_frete():
    cliente.post(
        "/carrinho/itens",
        json={"produto_id": 1, "quantidade": 1}
    )

    resposta = cliente.get("/carrinho/total")

    assert resposta.json()["total"] == 50.91