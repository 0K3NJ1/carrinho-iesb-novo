"""Verifica o código efetivo do notebook sem baixar o Qwen."""
import contextlib
import io
import json
import math
import runpy
from pathlib import Path

root = Path(__file__).resolve().parents[1]
with contextlib.redirect_stdout(io.StringIO()) as registro:
    anterior = runpy.run_path(str(root / 'work/verificar_unificado.py'))
ns = anterior['namespace']
ns['VIZINHOS'].pop('Isolado')
dados = ns['DADOS_TEMPO']
assert len(dados) == 24 * len(ns['LIGACOES']) and dados.trecho.nunique() == len(ns['LIGACOES'])
assert dados.equals(ns['gerar_dados_sinteticos']())
assert dados.velocidade_base_kmh.eq(15).all()
# Mesmas observações e semente: a única alteração no alvo é a base 10 -> 15 km/h.
antigos = ns['pd'].read_csv(root / 'work/resultados_fase2/tempos_sinteticos.csv')
for coluna in ['trecho', 'origem', 'destino', 'distancia_m', 'fluxo', 'piso', 'porta', 'obstaculo', 'repeticao']:
    assert dados[coluna].equals(antigos[coluna]), coluna
fator = 1 + 0.15 * dados.fluxo + 0.25 * dados.piso.eq('irregular')
esperado = antigos.tempo_s - dados.distancia_m * 3.6 * (1 / 10 - 1 / 15) * fator
nao_limitado = antigos.tempo_s > 0.1
assert ns['np'].allclose(dados.loc[nao_limitado, 'tempo_s'], esperado[nao_limitado].clip(lower=0.1))
assert set(ns['treino'].trecho).isdisjoint(ns['teste'].trecho)
for treino, validacao in ns['GroupKFold'](5).split(ns['treino'], groups=ns['treino'].trecho):
    assert set(ns['treino'].iloc[treino].trecho).isdisjoint(ns['treino'].iloc[validacao].trecho)
assert len(ns['COMPARACAO_MODELOS']) == 2
for r in ns['COMPARACAO_MODELOS']:
    assert all(math.isfinite(r[k]) for k in ['mae_s', 'rmse_s', 'r2'])
nos = ns['LOCAIS']
for cenario in ['tranquilo', 'movimentado', 'cadeiras_no_patio']:
    grafo = ns['prever_grafo_tempo'](cenario)
    dist = {a: {b: 0 if a == b else math.inf for b in nos} for a in nos}
    for a in nos:
        assert {b for b, _ in grafo[a]} == {b for b, _ in ns['VIZINHOS'][a]}
        for b, custo in grafo[a]:
            assert math.isfinite(custo) and custo > 0
            dist[a][b] = custo
    for k in nos:
        for a in nos:
            for b in nos:
                dist[a][b] = min(dist[a][b], dist[a][k] + dist[k][b])
    referencia = {a: ns['buscar']('Entrada Principal', a, grafo, False)[1] for a in nos}
    for a in nos:
        for b in nos:
            caminho, custo, _ = ns['buscar'](a, b, grafo, True, referencia)
            assert math.isclose(custo, dist[a][b], abs_tol=1e-8)
            assert caminho[0] == a and caminho[-1] == b
            assert math.isclose(sum(dict(grafo[x])[y] for x, y in zip(caminho, caminho[1:])), custo, abs_tol=1e-8)
            h = abs(referencia[a] - referencia[b])
            assert h <= dist[a][b] + 1e-8
            for v, peso in grafo[a]:
                assert h <= peso + abs(referencia[v] - referencia[b]) + 1e-8
    pedido = {'name': 'rota_tempo_previsto', 'arguments': dict(origem='Entrada Principal', destino='Mesa 4', cenario=cenario)}
    assert 'SINTÉTICO' in ns['executar'](pedido)
assert ns['rota_tempo_previsto']('Entrada Principal', 'Mesa 4', 'invalido').startswith('Erro:')
assert ns['rota_tempo_previsto']('Local falso', 'Mesa 4').startswith('Erro:')
assert ns['rota_tempo_previsto'] in ns['FERRAMENTAS']
demo = ns['DEMONSTRACAO_PATIO']
assert demo['mudou'] and demo['distancia_m'] < demo['distancia_rota_tempo_m']
assert demo['tempo_previsto_s'] < demo['tempo_rota_curta_s']
saida = ns['rota_tempo_previsto']('Mesa 1', 'Mesa 4', 'cadeiras_no_patio')
assert f"{demo['distancia_rota_tempo_m']:.1f} m" in saida
assert f"{demo['tempo_previsto_s']:.1f} s" in saida
assert '15 km/h' in saida
assert '0.0 m' in ns['rota_tempo_previsto']('Mesa 4', 'Mesa 4')
tranquilo = ns['prever_grafo_tempo']('tranquilo')
cadeiras = ns['prever_grafo_tempo']('cadeiras_no_patio')
for a, b, _ in ns['LIGACOES']:
    if {a, b} == {'Pátio - A', 'Pátio - B'}:
        assert dict(cadeiras[a])[b] > dict(tranquilo[a])[b]
    else:
        assert math.isclose(dict(cadeiras[a])[b], dict(tranquilo[a])[b], abs_tol=1e-8)
mensagem = (f'OK: regressão dos {len(nos)**2} pares em metros; geração reproduzível; grupos sem vazamento; '
            f'dois modelos; {3 * len(nos)**2} pares em segundos contra Floyd-Warshall; heurística admissível e consistente; '
            'conectividade preservada; despacho da ferramenta. Qwen e Colab não executados.')
print(registro.getvalue())
print(mensagem)
(ns['PASTA_FASE2'] / 'verificacao.txt').write_text(mensagem + '\n', encoding='utf-8')
