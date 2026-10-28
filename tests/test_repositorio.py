
import pytest
from sqlmodel import Session

from loja.banco import criar_tabelas, engine_em_memoria
from loja.produto import Calca, Camiseta
from loja.repositorio import RepositorioProdutos


@pytest.fixture
def repositorio():
    engine = engine_em_memoria()
    criar_tabelas(engine)

    with Session(engine) as sessao:
        yield RepositorioProdutos(sessao)

    engine.dispose()


def test_adicionar_e_buscar(repositorio):
    produto = Camiseta("Camiseta teste", 39.90, "M", "curta")
    produto_id = repositorio.adicionar(produto)

    encontrado = repositorio.buscar(produto_id)

    assert encontrado.nome == "Camiseta teste"
    assert encontrado.manga == "curta"


def test_buscar_inexistente(repositorio):
    assert repositorio.buscar(999) is None


def test_listar_com_filtros(repositorio):
    repositorio.adicionar(Camiseta("Camiseta A", 39.90, "M", "curta"))
    repositorio.adicionar(Calca("Calca B", 129.90, "G", "reta"))

    resultado = repositorio.listar(tamanho="M")

    assert len(resultado) == 1
    assert resultado[0][1].nome == "Camiseta A"


def test_existe_nome(repositorio):
    repositorio.adicionar(Camiseta("Camiseta C", 49.90, "P", "longa"))

    assert repositorio.existe_nome("Camiseta C")
    assert not repositorio.existe_nome("Outro produto")


def test_atualizar(repositorio):
    produto_id = repositorio.adicionar(
        Camiseta("Camiseta D", 39.90, "M", "curta")
    )

    atualizado = repositorio.atualizar(
        produto_id,
        Camiseta("Camiseta D nova", 49.90, "G", "longa"),
    )

    assert atualizado is True
    assert repositorio.buscar(produto_id).nome == "Camiseta D nova"


def test_remover(repositorio):
    produto_id = repositorio.adicionar(
        Camiseta("Camiseta E", 39.90, "M", "curta")
    )

    assert repositorio.remover(produto_id) is True
    assert repositorio.buscar(produto_id) is None
