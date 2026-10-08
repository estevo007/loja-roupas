from .calculos import total_carrinho, frete
from .produto import Produto
from .promocao import SemPromocao, Promocao


class Carrinho:
    def __init__(self, promocao=None):
        self._itens = []
        self._finalizado = False

        if promocao is not None and not isinstance(promocao, Promocao):
            raise TypeError("promoção deve seguir o contrato Promocao")

        self.promocao = promocao or SemPromocao()

    def adicionar(self, produto, quantidade=1):
        if self._finalizado:
            raise RuntimeError("carrinho já finalizado")

        if not isinstance(produto, Produto):
            raise TypeError("produto inválido")

        if quantidade <= 0:
            raise ValueError("quantidade deve ser maior que zero")

        self._itens.append((produto, quantidade))

    @property
    def itens(self):
        return list(self._itens)

    @property
    def quantidade_de_pecas(self):
        return sum(quantidade for _, quantidade in self._itens)

    @property
    def subtotal(self):
        return total_carrinho(
            [(produto.preco, quantidade) for produto, quantidade in self._itens]
        )

    @property
    def total(self):
        com_desconto = self.promocao.aplicar(self.subtotal)
        return com_desconto + frete(com_desconto)

    def finalizar(self):
        if not self._itens:
            raise ValueError("não é possível finalizar um carrinho vazio")

        self._finalizado = True