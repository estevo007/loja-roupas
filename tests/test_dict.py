from loja.produto import Calca, Camiseta, Produto


def test_produto_vira_dicionario():
    moletom = Produto("Moletom", 159.90, "P")

    assert moletom.para_dict() == {
        "tipo": "Produto",
        "nome": "Moletom",
        "preco": 159.90,
        "tamanho": "P",
    }


def test_camiseta_acrescenta_a_manga():
    camiseta = Camiseta("Camiseta básica", 39.90, "M", "curta")
    dados = camiseta.para_dict()

    assert dados["tipo"] == "Camiseta"
    assert dados["manga"] == "curta"


def test_calca_acrescenta_a_modelagem():
    calca = Calca("Calça jeans", 129.90, "G", "reta")

    assert calca.para_dict()["modelagem"] == "reta"