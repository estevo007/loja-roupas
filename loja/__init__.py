def __init__(self, promocao=None):
    self._itens = []
    self._finalizado = False

    if promocao is not None and not isinstance(promocao, Promocao):
        raise TypeError("promoção deve seguir o contrato Promocao")

    self.promocao = promocao or SemPromocao()