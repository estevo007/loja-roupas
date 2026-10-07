"""Etapa 3: funções puras, fáceis de testar (Aula 4)."""


FRETE_FIXO = 15.0
FRETE_GRATIS_A_PARTIR_DE = 200.0

def frete(valor_da_compra):
    """Frete grátis a partir de R$ 200; abaixo disso, R$ 15."""
    if valor_da_compra >= FRETE_GRATIS_A_PARTIR_DE:
        return 0.0
    return FRETE_FIXO


def total_carrinho(itens):
    """Recebe uma lista de (preço, quantidade) e devolve o total."""

    total = 0
    for preco, quantidade in itens:
        total = total + preco * quantidade
    return total

