
from html.parser import HTMLParser
from pathlib import Path

import pytest


class LeitorHTML(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))


def ler(pagina):
    leitor = LeitorHTML()
    leitor.feed(pagina.read_text(encoding="utf-8"))
    return leitor.tags


PASTA_FRONT = Path(__file__).parents[1] / "front"
PAGINAS = list(PASTA_FRONT.glob("*.html"))
CADASTRO = PASTA_FRONT / "cadastro.html"


@pytest.fixture(params=PAGINAS)
def pagina(request):
    return request.param


def test_estrutura_semantica(pagina):
    nomes = [tag for tag, _ in ler(pagina)]

    for tag in ("header", "nav", "main", "footer"):
        assert tag in nomes, f"falta <{tag}>"

    assert nomes.count("main") == 1
    assert nomes.count("h1") == 1


def test_toda_imagem_tem_alt(pagina):
    for tag, atributos in ler(pagina):
        if tag == "img":
            assert "alt" in atributos


def test_cadastro_tem_os_quatro_campos():
    tags = ler(CADASTRO)

    campos = {
        atributos.get("name")
        for tag, atributos in tags
        if tag in ("input", "select")
    }

    assert {"tipo", "nome", "preco", "tamanho"}.issubset(campos)


def test_cadastro_tem_labels_para_todos_os_campos():
    tags = ler(CADASTRO)

    ids_campos = {
        atributos.get("id")
        for tag, atributos in tags
        if tag in ("input", "select")
    }

    labels = {
        atributos.get("for")
        for tag, atributos in tags
        if tag == "label"
    }

    assert {"tipo", "nome", "preco", "tamanho"}.issubset(labels)
    assert labels.issubset(ids_campos)


def test_cadastro_tem_campos_obrigatorios():
    tags = ler(CADASTRO)

    campos_obrigatorios = {
        atributos.get("name")
        for tag, atributos in tags
        if tag in ("input", "select") and "required" in atributos
    }

    assert {"nome", "preco", "tamanho", "tipo"}.issubset(
        campos_obrigatorios
    )


def test_cadastro_tem_botao_de_envio():
    tags = ler(CADASTRO)

    botoes = [
        atributos
        for tag, atributos in tags
        if tag == "button"
    ]

    assert any(
        atributos.get("type") == "submit"
        for atributos in botoes
    )
