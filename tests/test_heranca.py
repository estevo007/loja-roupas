

import pytest

from loja.produto import Camiseta


def test_camiseta_herda_a_validacao_do_produto():
    with pytest.raises(ValueError):
        Camiseta("Camiseta básica", -10, "M", "curta")

def test_manga_invalida():
    with pytest.raises(ValueError):
        Camiseta("Camiseta básica", 39.90, "M", "regata")

def test_camiseta_descricao_com_manga():
    camiseta = Camiseta("Camiseta básica", 39.90, "M", "curta")

    assert camiseta.descricao() == "Camiseta básica M: R$ 39.90 · manga curta"


def test_camiseta_manga_longa():
    camiseta = Camiseta("Camiseta básica", 39.90, "M", "longa")

    assert camiseta.manga == "longa"