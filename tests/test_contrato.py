import pytest

from loja.promocao import Promocao
from loja.carrinho import Carrinho


def test_promocao_sem_aplicar_nao_nasce():
    class BlackFriday(Promocao):
        def aplicar_desconto(self, subtotal):
            return subtotal * 0.5

    with pytest.raises(TypeError):
        BlackFriday()


def test_carrinho_recusa_quem_nao_segue_o_contrato():
    class Parecida:
        def aplicar(self, subtotal):
            return subtotal

    with pytest.raises(TypeError):
        Carrinho(Parecida())