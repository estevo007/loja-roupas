import pytest

from loja.calculos import total_carrinho
from loja.calculos import frete

def test_carrinho_vazio_custa_zero():
    assert total_carrinho([]) == 0

def test_soma_preco_vezes_quantidade():

    itens = [(39.90, 3), (129.90, 1)]

    total = total_carrinho(itens)

    assert total == pytest.approx(249.60)

def test_frete_abaixo_de_200_custa_15():
    assert frete(199.99) == 15.0


def test_frete_a_partir_de_200_e_gratis():
    assert frete(200.00) == 0.0
    assert frete(350.00) == 0.0
