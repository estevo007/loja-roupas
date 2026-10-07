

import pytest

from loja.produto import Camiseta


def test_camiseta_herda_a_validacao_do_produto():
    with pytest.raises(ValueError):
        Camiseta("Camiseta básica", -10, "M", "curta")

def test_manga_invalida():
    with pytest.raises(ValueError):
        Camiseta("Camiseta básica", 39.90, "M", "regata")