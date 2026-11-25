"""Executa as Fases 1 e 2 do notebook original e grava dados reais para as animações.

O notebook não é modificado: as células são lidas e executadas num namespace separado.
A busca é acompanhada por uma cópia de `buscar` que registra cada iteração; o script
confere que a cópia devolve exatamente o mesmo caminho, custo e expansões do original.

Uso: python ferramentas/tracos.py   (grava dados/tracos.json)
"""
import json
import os
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
NOTEBOOK = RAIZ.parent / 'carrinho_iesb_unificado.ipynb'
TRABALHO = RAIZ / 'cache' / 'execucao_fases'


def executar_celulas(ate):
    nb = json.loads(NOTEBOOK.read_text(encoding='utf-8'))
    ns = {}
    TRABALHO.mkdir(parents=True, exist_ok=True)
    os.chdir(TRABALHO)          # arquivos gerados pelo notebook ficam no cache
    import matplotlib
    matplotlib.use('Agg')
    for i, c in enumerate(nb['cells'][:ate]):
        if c['cell_type'] != 'code':
            continue
        fonte = '\n'.join(l for l in ''.join(c['source']).split('\n') if not l.strip().startswith('%'))
        exec(compile(fonte, f'celula_{i}', 'exec'), ns)
    return ns


def buscar_com_traco(origem, destino, grafo, usar_heuristica, referencia):
    """Mesma lógica de `buscar` (célula 7), registrando a fronteira a cada iteração."""
    passos = []
    estimativa = abs(referencia.get(origem, 0) - referencia.get(destino, 0)) if usar_heuristica else 0
    fronteira = [(estimativa, 0, origem, [origem])]
    visitados = []
    expandidos = 0
    while len(fronteira) > 0:
        melhor = min(fronteira)
        passo = dict(fronteira=[dict(f=round(f, 2), g=round(g, 2), h=round(f - g, 2), local=l, caminho=c)
                                for f, g, l, c in sorted(fronteira)],
                     escolhido=dict(f=round(melhor[0], 2), g=round(melhor[1], 2), local=melhor[2], caminho=melhor[3]),
                     visitados=list(visitados))
        fronteira.remove(melhor)
        f, g, local, caminho = melhor
        if local == destino:
            passo['acao'] = 'objetivo'
            passos.append(passo)
            return caminho, g, expandidos, passos
        if local in visitados:
            passo['acao'] = 'ja_visitado'
            passos.append(passo)
            continue
        visitados.append(local)
        expandidos = expandidos + 1
        novos = []
        for vizinho, custo in grafo[local]:
            if vizinho not in visitados:
                novo_g = g + custo
                estimativa = abs(referencia.get(vizinho, 0) - referencia.get(destino, 0)) if usar_heuristica else 0
                fronteira.append((novo_g + estimativa, novo_g, vizinho, caminho + [vizinho]))
                novos.append(dict(local=vizinho, custo_aresta=round(custo, 2), g=round(novo_g, 2),
                                  h=round(estimativa, 2), f=round(novo_g + estimativa, 2)))
        passo['acao'] = 'expandiu'
        passo['novos'] = novos
        passos.append(passo)
    return None, None, expandidos, passos


def traco(ns, origem, destino, grafo, usar_h, referencia):
    caminho, custo, expandidos, passos = buscar_com_traco(origem, destino, grafo, usar_h, referencia)
    original = ns['buscar'](origem, destino, grafo, usar_h, referencia)
    assert (caminho, custo, expandidos) == original, (caminho, custo, expandidos, original)
    return dict(origem=origem, destino=destino, usar_heuristica=usar_h, caminho=caminho,
                custo=round(custo, 2), expandidos=expandidos, passos=passos)


def main():
    ns = executar_celulas(20)   # até a célula 19 (Fase 2), sem carregar o Qwen
    D = ns['DISTANCIA_ENTRADA']
    grafo_cadeiras = ns['prever_grafo_tempo']('cadeiras_no_patio')
    grafo_tranquilo = ns['prever_grafo_tempo']('tranquilo')
    ref_cadeiras = {l: ns['buscar']('Entrada Principal', l, grafo_cadeiras, False)[1] for l in ns['LOCAIS']}
    patio = ['Pátio - A', 'Pátio - B', 'Pátio/Direito', 'Pátio - D', 'Mesa 1', 'Mesa 2', 'Mesa 3', 'Mesa 4']
    tempos_patio = {}
    for nome, g in [('tranquilo', grafo_tranquilo), ('cadeiras_no_patio', grafo_cadeiras)]:
        tempos_patio[nome] = {f'{a}|{b}': round(dict(g[a])[b], 2) for a, b, _ in ns['LIGACOES']
                              if a in patio and b in patio}
    dados = ns['DADOS_TEMPO']
    saida = dict(
        locais=ns['LOCAIS'], ligacoes=[list(l) for l in ns['LIGACOES']],
        distancia_entrada={k: round(v, 2) for k, v in D.items()},
        tempo_preparo_ms=round(ns['TEMPO_PREPARO_MS'], 3),
        ucs_mesa1_mesa4=traco(ns, 'Mesa 1', 'Mesa 4', ns['VIZINHOS'], False, D),
        astar_mesa1_mesa4=traco(ns, 'Mesa 1', 'Mesa 4', ns['VIZINHOS'], True, D),
        ucs_entrada_mesa4=traco(ns, 'Entrada Principal', 'Mesa 4', ns['VIZINHOS'], False, D),
        astar_entrada_mesa4=traco(ns, 'Entrada Principal', 'Mesa 4', ns['VIZINHOS'], True, D),
        astar_biblioteca_c02=traco(ns, 'Biblioteca', 'C-02', ns['VIZINHOS'], True, D),
        ucs_biblioteca_c02=traco(ns, 'Biblioteca', 'C-02', ns['VIZINHOS'], False, D),
        astar_cadeiras_mesa1_mesa4=traco(ns, 'Mesa 1', 'Mesa 4', grafo_cadeiras, True, ref_cadeiras),
        tempos_patio=tempos_patio,
        experimento=ns['RESULTADOS'],
        recortes={str(t): sorted(ns['recortar_mapa'](t)) for t in [20, 40, 70]},
        calcular_rota=ns['calcular_rota']('Entrada Principal', 'Mesa 4'),
        rota_tranquilo=ns['rota_tempo_previsto']('Entrada Principal', 'Mesa 4', 'tranquilo'),
        rota_movimentado=ns['rota_tempo_previsto']('Entrada Principal', 'Mesa 4', 'movimentado'),
        demonstracao_patio=ns['DEMONSTRACAO_PATIO'],
        validacao=ns['COMPARACAO_MODELOS'], escolhido=ns['MELHOR_MODELO'], teste=ns['METRICAS_TESTE'],
        dados_linhas=len(dados), dados_amostra=json.loads(dados.head(6).to_json(orient='records', force_ascii=False)),
        dados_colunas=list(dados.columns),
        vizinhos_patio=ns['listar_vizinhos']('Pátio/Direito'),
        calcular_tempo_exemplo=ns['calcular_tempo'](89.5, 15.0),
    )
    destino = RAIZ / 'dados' / 'tracos.json'
    destino.write_text(json.dumps(saida, ensure_ascii=False, indent=1, default=str), encoding='utf-8')
    for k in ['ucs_mesa1_mesa4', 'astar_mesa1_mesa4', 'ucs_entrada_mesa4', 'astar_entrada_mesa4',
              'ucs_biblioteca_c02', 'astar_biblioteca_c02', 'astar_cadeiras_mesa1_mesa4']:
        t = saida[k]
        print(f"{k}: custo {t['custo']} expandidos {t['expandidos']} iterações {len(t['passos'])} caminho {t['caminho']}")
    print('tempos pátio', saida['tempos_patio'])


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
