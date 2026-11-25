"""Inventário do código do notebook: células, importações, funções, chamadas e variáveis globais.

Lê o notebook original sem modificá-lo e grava dados/inventario.json.
Uso: python ferramentas/inventario.py
"""
import ast
import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
NOTEBOOK = RAIZ.parent / 'carrinho_iesb_unificado.ipynb'


def celulas_de_codigo():
    nb = json.loads(NOTEBOOK.read_text(encoding='utf-8'))
    for indice, celula in enumerate(nb['cells']):
        if celula['cell_type'] != 'code':
            continue
        fonte = ''.join(celula['source'])
        # Linhas mágicas do Jupyter (%pip) não são Python: viram comentário para o ast.
        linhas = ['# ' + l if l.strip().startswith('%') else l for l in fonte.split('\n')]
        yield indice, fonte, '\n'.join(linhas)


def nomes_chamados(no):
    chamados = set()
    for filho in ast.walk(no):
        if isinstance(filho, ast.Call):
            alvo = filho.func
            if isinstance(alvo, ast.Name):
                chamados.add(alvo.id)
            elif isinstance(alvo, ast.Attribute):
                chamados.add('.' + alvo.attr)
    return chamados


def main():
    celulas, funcoes, importacoes, globais = [], [], [], {}
    for indice, fonte, python in celulas_de_codigo():
        arvore = ast.parse(python)
        celulas.append(dict(celula=indice, linhas=fonte.count('\n') + 1, primeira_linha=fonte.split('\n')[0]))
        for no in ast.walk(arvore):
            if isinstance(no, ast.Import):
                for a in no.names:
                    importacoes.append(dict(celula=indice, modulo=a.name, nome=a.asname or a.name))
            elif isinstance(no, ast.ImportFrom):
                for a in no.names:
                    importacoes.append(dict(celula=indice, modulo=no.module, nome=a.name))
        for no in arvore.body:
            if isinstance(no, ast.FunctionDef):
                funcoes.append(dict(
                    nome=no.name, celula=indice, linha_inicio=no.lineno, linha_fim=no.end_lineno,
                    parametros=[a.arg for a in no.args.args],
                    padroes=[ast.unparse(d) for d in no.args.defaults],
                    docstring=(ast.get_docstring(no) or '').split('\n')[0],
                    chama=sorted(nomes_chamados(no)),
                    tem_return=any(isinstance(n, ast.Return) for n in ast.walk(no)),
                    tem_while=any(isinstance(n, ast.While) for n in ast.walk(no)),
                    tem_for=any(isinstance(n, ast.For) for n in ast.walk(no)),
                    tem_try=any(isinstance(n, ast.Try) for n in ast.walk(no)),
                ))
            elif isinstance(no, (ast.Assign, ast.AnnAssign)):
                alvos = no.targets if isinstance(no, ast.Assign) else [no.target]
                for alvo in alvos:
                    for nome in ast.walk(alvo):
                        if isinstance(nome, ast.Name):
                            globais.setdefault(nome.id, []).append(indice)
    nomes = {f['nome'] for f in funcoes}
    for f in funcoes:
        f['chama_do_projeto'] = sorted(n for n in f['chama'] if n in nomes)
        f['chamada_por'] = sorted(g['nome'] for g in funcoes if f['nome'] in g['chama'])
    saida = dict(notebook=str(NOTEBOOK.name), celulas=celulas, importacoes=importacoes,
                 funcoes=funcoes, globais=globais)
    destino = RAIZ / 'dados' / 'inventario.json'
    destino.parent.mkdir(exist_ok=True)
    destino.write_text(json.dumps(saida, ensure_ascii=False, indent=1), encoding='utf-8')
    print(len(celulas), 'células de código,', len(funcoes), 'funções,', len(importacoes), 'importações')
    for f in funcoes:
        print(f"  {f['nome']}({', '.join(f['parametros'])}) célula {f['celula']} "
              f"l.{f['linha_inicio']}-{f['linha_fim']} -> {f['chama_do_projeto']} | chamada por {f['chamada_por']}")
    print('importações:', sorted({(i['modulo'] or '') + ':' + i['nome'] for i in importacoes}))


if __name__ == '__main__':
    main()
