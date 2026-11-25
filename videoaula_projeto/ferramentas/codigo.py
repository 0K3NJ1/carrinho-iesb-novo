"""Converte as células de código do notebook em linhas HTML com cores (Pygments).

Grava dados/codigo.json: {"7": {"titulo": "...", "linhas": ["<span ...>", ...]}, ...}
Também é importado por construir.py para colorir exemplos que não estão no notebook.
"""
import html
import json
import re
from pathlib import Path

from pygments.lexers import PythonLexer
from pygments.token import Token

RAIZ = Path(__file__).resolve().parents[1]
NOTEBOOK = RAIZ.parent / 'carrinho_iesb_unificado.ipynb'

CLASSES = [
    (Token.Comment, 'cm'), (Token.Literal.String, 'st'), (Token.Literal.Number, 'nu'),
    (Token.Keyword.Constant, 'kc'), (Token.Keyword.Namespace, 'kn'), (Token.Keyword, 'kw'),
    (Token.Operator.Word, 'kw'), (Token.Name.Function, 'fn'), (Token.Name.Builtin.Pseudo, 'kc'),
    (Token.Name.Builtin, 'bi'), (Token.Name.Class, 'fn'), (Token.Name.Namespace, 'ns'),
    (Token.Name.Decorator, 'fn'), (Token.Operator, 'op'), (Token.Punctuation, 'pu'), (Token.Name, 'nm'),
]


def classe(tipo):
    for base, nome in CLASSES:
        if tipo in base:
            return nome
    return ''


def colorir(fonte):
    """Devolve uma lista de linhas HTML, uma por linha do código."""
    linhas, atual = [], []
    tokens = list(PythonLexer().get_tokens(fonte))
    anterior = None
    for tipo, valor in tokens:
        c = classe(tipo)
        # nome seguido de "(" vira chamada de função (amarelo, como no VS Code)
        partes = valor.split('\n')
        for k, parte in enumerate(partes):
            if k > 0:
                linhas.append(''.join(atual))
                atual = []
            if parte:
                texto = html.escape(parte)
                atual.append(f'<span class="{c}">{texto}</span>' if c else texto)
        anterior = (tipo, valor)
    linhas.append(''.join(atual))
    # o lexer acrescenta uma quebra de linha final: ajusta ao número real de linhas
    esperado = fonte.count('\n') + 1
    while len(linhas) > esperado and linhas[-1] == '':
        linhas.pop()
    while len(linhas) < esperado:
        linhas.append('')
    # chamadas: <span class="nm">x</span><span class="pu">(</span> -> fn
    linhas = [re.sub(r'<span class="nm">([^<]+)</span>(<span class="pu">\(</span>)',
                     r'<span class="fn">\1</span>\2', l) for l in linhas]
    return linhas


def main():
    nb = json.loads(NOTEBOOK.read_text(encoding='utf-8'))
    saida, titulo = {}, ''
    for i, c in enumerate(nb['cells']):
        fonte = ''.join(c['source'])
        if c['cell_type'] == 'markdown':
            for linha in fonte.split('\n'):
                if linha.startswith('#'):
                    titulo = linha.lstrip('#').strip()
                    break
            continue
        linhas = colorir(fonte)
        assert len(linhas) == fonte.count('\n') + 1, (i, len(linhas), fonte.count('\n') + 1)
        saida[str(i)] = dict(titulo=titulo, linhas=linhas, texto=fonte.split('\n'))
    (RAIZ / 'dados' / 'codigo.json').write_text(json.dumps(saida, ensure_ascii=False), encoding='utf-8')
    print(len(saida), 'células coloridas:', {k: len(v['linhas']) for k, v in saida.items()})


if __name__ == '__main__':
    main()
