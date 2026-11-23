import contextlib
import io
import json
import math
from pathlib import Path

root = Path(__file__).resolve().parents[1]
entrega = root / 'entrega_compartilhamento' if (root / 'entrega_compartilhamento').is_dir() else root
nb = json.loads((entrega / 'carrinho_iesb_unificado.ipynb').read_text())
namespace = {}
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] != 'code':
        continue
    source = ''.join(cell['source'])
    if source.startswith('%pip'):
        continue
    compile(source, f'cell_{i}', 'exec')
    # Sem baixar o LLM: executa mapa, busca, tempo, ferramentas e definições do agente.
    if any(text in source for text in ['import torch', 'from transformers.utils',
                                       'import matplotlib.pyplot', '# Executar somente após carregar o Qwen real']):
        continue
    if source.startswith('CASOS ='):
        # Define os casos e as referências, mas não chama o Qwen localmente.
        source = source.split('AVALIACOES =')[0]
    exec(source, namespace)

assert len(namespace['LOCAIS']) == 90
markdown = '\n'.join(''.join(cell['source']) for cell in nb['cells']
                     if cell['cell_type'] == 'markdown')
for item in ['Estado inicial', 'Função de transição', 'Teste de objetivo',
             'Custo do caminho', 'três mapas independentes',
             'tempo de preparação']:
    assert item in markdown
assert len(namespace['CASOS']) == 39
assert [case['id'] for case in namespace['CASOS']] == list(range(1, 40))
assert all('resultado_esperado' in case for case in namespace['CASOS'])
namespace['conversar'] = lambda mensagens, ferramentas=None, max_tokens=200: 'Resposta direta.'
detalhes = namespace['agente']('Bom dia!', mostrar=False, retornar_detalhes=True)
assert detalhes['resposta'] == 'Resposta direta.' and detalhes['chamadas'] == []
assert detalhes['status'] == 'resposta_livre' and detalhes['pendencia'] is None
edges = namespace['LIGACOES']
assert len(edges) == 90
assert len({frozenset((a, b)) for a, b, _ in edges}) == 90
assert 'Gastro' not in namespace['LOCAIS']
assert 'Café Mania' in namespace['LOCAIS']
assert sum(d for _, _, d in edges[:5]) == 210
# Preserva as ligações fora dos corredores subdivididos.
old = json.loads((entrega / 'Marco_2/agente_iesb.ipynb').read_text())
old_namespace = {}
with contextlib.redirect_stdout(io.StringIO()):
    exec(''.join(old['cells'][3]['source']), old_namespace)
# Correção de nome confirmada pelo usuário; topologia histórica preservada.
arestas_antigas = {
    frozenset('Easy Smart' if nome == 'Oasis Smart' else nome for nome in e)
    for e in old_namespace['LIGACOES']}
arestas_atuais = {frozenset((a, b)) for a, b, _ in edges}
destinos_internos = {f'{p}-{i:02d}' for p in 'DCBIJ' for i in range(1, 7)}
destinos_internos.update(['WC Masculino I', 'WC Feminino I', 'WC Masculino J', 'WC Feminino J'])
destinos_internos.update(['Mesa 1', 'Mesa 2', 'Mesa 3', 'Mesa 4', 'Gastro', 'Easy Smart'])
for aresta in arestas_antigas:
    if not aresta.intersection(destinos_internos):
        assert aresta in arestas_atuais
# Rotas entre portas vizinhas não retornam à entrada do corredor.
for prefixo, corredor in [('D', 'Corredor Design'), ('C', 'Corredor Bloco C'), ('B', 'Corredor Bloco B')]:
    caminho, custo = namespace['a_estrela'](prefixo + '-01', prefixo + '-02')
    assert corredor not in caminho and custo == 14
    assert caminho == [prefixo + '-01', corredor + ' - 01/04', corredor + ' - 02/05', prefixo + '-02']
assert namespace['a_estrela']('I-01', 'I-02')[1] == 14
assert namespace['a_estrela']('J-01', 'J-02')[1] == 14
assert namespace['a_estrela']('Pátio/Direito', 'D-01')[0][:4] == ['Pátio/Direito', 'Eixo - Norte', 'Eixo - Design', 'Corredor Design']

# Floyd-Warshall independente: confere custo ótimo de todos os 8.100 pares.
nodes = namespace['LOCAIS']
distance = {a: {b: (0 if a == b else math.inf) for b in nodes} for a in nodes}
for a, b, meters in edges:
    assert meters > 0
    distance[a][b] = distance[b][a] = meters
for k in nodes:
    for a in nodes:
        for b in nodes:
            distance[a][b] = min(distance[a][b], distance[a][k] + distance[k][b])
for a in nodes:
    for b in nodes:
        path, cost = namespace['a_estrela'](a, b)
        assert cost == distance[a][b]
        assert 0 <= namespace['h'](a, b) <= distance[a][b]
        for v, edge_cost in namespace['VIZINHOS'][a]:
            assert namespace['h'](a, b) <= edge_cost + namespace['h'](v, b)
        assert path[0] == a and path[-1] == b
        total = sum(dict(namespace['VIZINHOS'][x])[y] for x, y in zip(path, path[1:]))
        assert total == cost
assert namespace['calcular_tempo'](100, 10) == 36
assert namespace['calcular_tempo'](100, 15) == 24
assert namespace['calcular_tempo'](0, 10) == 0
for speed in [0, -10, float('nan'), float('inf'), '15', None, True]:
    try:
        namespace['calcular_tempo'](100, speed)
        raise AssertionError('Velocidade inválida aceita')
    except ValueError:
        pass
assert namespace['calcular_rota']('Local inexistente', 'Mesa 4').startswith('Erro:')
assert namespace['VELOCIDADE_BASE_KMH'] == 15
assert '21.5 s' in namespace['calcular_rota']('Entrada Principal', 'Mesa 4')
assert [f.__name__ for f in namespace['FERRAMENTAS']] == ['rota_tempo_previsto', 'listar_vizinhos']
for nome in ['ferramenta_do_trio', 'calcular_rota']:
    assert namespace['executar']({'name': nome, 'arguments': {
        'origem': 'Entrada Principal', 'destino': 'Mesa 4'}}).startswith('Erro:')
for velocidade in [10, 15, None]:
    assert namespace['executar']({'name': 'rota_tempo_previsto', 'arguments': {
        'origem': 'Mesa 1', 'destino': 'Mesa 4', 'velocidade_kmh': velocidade}}).startswith('Erro:')
assert 'Velocidade base fixa: 15 km/h' in namespace['executar']({
    'name': 'rota_tempo_previsto', 'arguments': {'origem': 'Mesa 1', 'destino': 'Mesa 4'}})
# Conferência do caso desconectado sem mudar o notebook.
namespace['VIZINHOS']['Isolado'] = []
assert namespace['a_estrela']('Entrada Principal', 'Isolado') == (None, None)
print(f'OK: sintaxe; {len(nodes)**2} pares; corredores subdivididos; demais acessos preservados; tempos e despacho.')
print('Qwen não carregado; inferência e execução completa no Colab ainda não verificadas nesta versão.')

for tamanho in [20, 40, 70]:
    resultados = [r for r in namespace['RESULTADOS'] if r['nos'] == tamanho]
    assert len(resultados) == 2
    assert resultados[0]['custo_m'] == resultados[1]['custo_m']
    assert all(r['execucao_ms'] > 0 for r in resultados)
    assert all(0 < r['expandidos'] < tamanho for r in resultados)
(root / 'work/graficos/resultados.json').write_text(json.dumps(namespace['RESULTADOS'], ensure_ascii=False, indent=2))
print('OK: heurística admissível e consistente em todos os pares; 3 tamanhos, 2 buscas. Renderização dos gráficos não executada por este verificador.')
