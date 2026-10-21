
TAMANHOS = ("PP", "P", "M", "G", "GG")


class Produto:
    def __init__(self, nome, preco, tamanho):
        if not nome or not nome.strip():
            raise ValueError("nome do produto não pode ser vazio")
        if preco <= 0:
            raise ValueError("preço deve ser maior que zero")
        if tamanho not in TAMANHOS:
            raise ValueError(f"tamanho inválido: {tamanho}")

        self.nome = nome.strip()
        self.preco = preco
        self.tamanho = tamanho

    def descricao(self):
        return f"{self.nome} {self.tamanho}: R$ {self.preco:.2f}"

    def para_dict(self):
        """O produto em formato de dicionário, pronto para virar JSON."""
        return {
            "tipo": type(self).__name__,
            "nome": self.nome,
            "preco": self.preco,
            "tamanho": self.tamanho,
        }


class Camiseta(Produto):
    MANGAS = ("curta", "longa")

    def __init__(self, nome, preco, tamanho, manga):
        super().__init__(nome, preco, tamanho)

        if manga not in self.MANGAS:
            raise ValueError(f"manga inválida: {manga}")

        self.manga = manga

    def descricao(self):
        return f"{super().descricao()} · manga {self.manga}"

    def para_dict(self):
        dados = super().para_dict()
        dados["manga"] = self.manga
        return dados


class Calca(Produto):
    def __init__(self, nome, preco, tamanho, modelagem):
        super().__init__(nome, preco, tamanho)
        self.modelagem = modelagem

    def descricao(self):
        return f"{super().descricao()} · {self.modelagem}"

    def para_dict(self):
        dados = super().para_dict()
        dados["modelagem"] = self.modelagem
        return dados