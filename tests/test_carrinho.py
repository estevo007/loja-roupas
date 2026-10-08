import pytest

from loja.carrinho import Carrinho
from loja.produto import Produto


def carrinho_exemplo():
    c = Carrinho()
    c.adicionar(Produto("Camiseta básica", 39.90, "M"), 3)
    c.adicionar(Produto("Calça jeans", 129.90, "G"))
    return c


def test_subtotal_e_quantidade():
    c = carrinho_exemplo()
    assert c.quantidade_de_pecas == 4
    assert c.subtotal == pytest.approx(249.60)


def test_acima_de_200_frete_gratis():
    assert carrinho_exemplo().total == pytest.approx(249.60)


def test_nao_pode_adicionar_depois_de_finalizar():
    c = Carrinho()
    c.adicionar(Produto("Camiseta básica", 39.90, "M"))
    c.finalizar()

    with pytest.raises(RuntimeError):
        c.adicionar(Produto("Calça jeans", 129.90, "G"))


def test_produto_invalido():
    c = Carrinho()

    with pytest.raises(TypeError):
        c.adicionar("produto inválido")


def test_quantidade_invalida():
    c = Carrinho()
    produto = Produto("Camiseta básica", 39.90, "M")

    with pytest.raises(ValueError):
        c.adicionar(produto, 0)


def test_itens_devolve_copia():
    c = Carrinho()
    produto = Produto("Camiseta básica", 39.90, "M")
    c.adicionar(produto)

    itens = c.itens
    itens.clear()

    assert c.quantidade_de_pecas == 1