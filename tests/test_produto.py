import pytest

from loja.produto import Produto

def test_produto_valido():
    camiseta = Produto("Camiseta básica", 39.90, "M")
    assert camiseta.descricao() == "Camiseta básica M: R$ 39.90"

def test_preco_zero_nao_e_aceito():
    with pytest.raises(ValueError):
        Produto("Camiseta básica", 0, "M")