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