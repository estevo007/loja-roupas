
from sqlmodel import Session, select

from loja.banco import ProdutoRegistro
from loja.produto import Calca, Camiseta, Produto


CAMPOS = ("tipo", "nome", "preco", "tamanho", "manga", "modelagem")


def para_dominio(registro):
    if registro.tipo == "Camiseta":
        return Camiseta(
            registro.nome,
            registro.preco,
            registro.tamanho,
            registro.manga,
        )

    if registro.tipo == "Calca":
        return Calca(
            registro.nome,
            registro.preco,
            registro.tamanho,
            registro.modelagem,
        )

    return Produto(registro.nome, registro.preco, registro.tamanho)


def para_registro(produto):
    return ProdutoRegistro(**produto.para_dict())


class RepositorioProdutos:

    def __init__(self, sessao: Session):
        self.sessao = sessao

    def adicionar(self, produto):
        registro = para_registro(produto)
        self.sessao.add(registro)
        self.sessao.commit()
        self.sessao.refresh(registro)
        return registro.id

    def buscar(self, produto_id):
        registro = self.sessao.get(ProdutoRegistro, produto_id)
        if registro is None:
            return None
        return para_dominio(registro)

    def existe_nome(self, nome, exceto_id=None):
        consulta = select(ProdutoRegistro).where(
            ProdutoRegistro.nome == nome
        )
        registro = self.sessao.exec(consulta).first()
        return registro is not None and registro.id != exceto_id

    def listar(self, tamanho=None, preco_max=None):
        consulta = select(ProdutoRegistro)

        if tamanho is not None:
            consulta = consulta.where(
                ProdutoRegistro.tamanho == tamanho
            )

        if preco_max is not None:
            consulta = consulta.where(
                ProdutoRegistro.preco <= preco_max
            )

        consulta = consulta.order_by(ProdutoRegistro.id)

        return [
            (registro.id, para_dominio(registro))
            for registro in self.sessao.exec(consulta)
        ]

    def atualizar(self, produto_id, produto):
        registro = self.sessao.get(ProdutoRegistro, produto_id)

        if registro is None:
            return False

        novo = para_registro(produto)

        for campo in CAMPOS:
            setattr(registro, campo, getattr(novo, campo))

        self.sessao.add(registro)
        self.sessao.commit()
        return True

    def remover(self, produto_id):
        registro = self.sessao.get(ProdutoRegistro, produto_id)

        if registro is None:
            return False

        self.sessao.delete(registro)
        self.sessao.commit()
        return True
