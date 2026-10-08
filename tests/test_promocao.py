import pytest

from loja.carrinho import Carrinho
from loja.produto import Produto
from loja.promocao import SemPromocao, Percentual, Cupom


def carrinho_com(promocao):
    c = Carrinho(promocao)
    c.adicionar(Produto("Camiseta básica", 39.90, "M"), 3)
    c.adicionar(Produto("Calça jeans", 129.90, "G"))
    return c  # subtotal 249.60


@pytest.mark.parametrize("promocao, esperado", [
    (SemPromocao(), 249.60),  # frete grátis
    (Percentual(10), 224.64),  # ainda acima de 200
    (Cupom(100), 164.60),  # 149.60 + 15 de frete
])
def test_total_com_cada_promocao(promocao, esperado):
    assert carrinho_com(promocao).total == pytest.approx(esperado)

def test_percentual_zero_mantem_o_valor():
    promocao = Percentual(0)

    assert promocao.aplicar(100) == 100


def test_percentual_cem_zera_o_valor():
    promocao = Percentual(100)

    assert promocao.aplicar(100) == 0


def test_percentual_acima_de_cem_e_invalido():
    with pytest.raises(ValueError):
        Percentual(101)


def test_percentual_negativo_e_invalido():
    with pytest.raises(ValueError):
        Percentual(-1)


def test_cupom_negativo_e_invalido():
    with pytest.raises(ValueError):
        Cupom(-10)


def test_cupom_maior_que_o_subtotal_nao_deixa_total_negativo():
    promocao = Cupom(200)

    assert promocao.aplicar(100) == 0


def test_sem_promocao_mantem_o_valor():
    promocao = SemPromocao()

    assert promocao.aplicar(100) == 100