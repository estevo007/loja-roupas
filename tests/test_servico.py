
import pytest
from sqlmodel import Session

from loja.banco import criar_tabelas, engine_em_memoria
from loja.repositorio import RepositorioProdutos
from loja.servico import (
    DadosInvalidos,
    ProdutoJaExiste,
    ProdutoNaoEncontrado,
    ServicoCatalogo,
)


CAMISETA = {
    "tipo": "Camiseta",
    "nome": "Camiseta teste",
    "preco": 39.90,
    "tamanho": "M",
    "manga": "curta",
}


@pytest.fixture
def servico():
    engine = engine_em_memoria()
    criar_tabelas(engine)

    with Session(engine) as sessao:
        yield ServicoCatalogo(RepositorioProdutos(sessao))

    engine.dispose()


def test_cadastrar_produto(servico):
    produto = servico.cadastrar(CAMISETA)

    assert produto["id"] == 1
    assert produto["nome"] == "Camiseta teste"
    assert produto["tipo"] == "Camiseta"


def test_listar_produtos(servico):
    servico.cadastrar(CAMISETA)

    produtos = servico.listar()

    assert len(produtos) == 1
    assert produtos[0]["nome"] == "Camiseta teste"


def test_nome_repetido_nao_entra(servico):
    servico.cadastrar(CAMISETA)

    with pytest.raises(ProdutoJaExiste):
        servico.cadastrar(CAMISETA)


def test_regra_do_dominio_vira_dados_invalidos(servico):
    with pytest.raises(DadosInvalidos):
        servico.cadastrar({**CAMISETA, "preco": 0})


def test_tipo_desconhecido_e_invalido(servico):
    with pytest.raises(DadosInvalidos):
        servico.cadastrar({**CAMISETA, "tipo": "Sapato"})


def test_buscar_inexistente(servico):
    with pytest.raises(ProdutoNaoEncontrado):
        servico.buscar(99)


def test_remover_inexistente(servico):
    with pytest.raises(ProdutoNaoEncontrado):
        servico.remover(99)
