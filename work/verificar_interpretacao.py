"""Testes com extração simulada. Não medem a interpretação do Qwen real."""
import contextlib
import io
import json
import runpy
from pathlib import Path

root = Path(__file__).resolve().parents[1]
with contextlib.redirect_stdout(io.StringIO()):
    ns = runpy.run_path(str(root / 'work/verificar_unificado.py'))['namespace']
ns['VIZINHOS'].pop('Isolado')


def chamada(nome, argumentos):
    return '<tool_call>' + json.dumps(dict(name=nome, arguments=argumentos), ensure_ascii=False) + '</tool_call>'


def respostas_controladas(respostas):
    fila = iter(respostas)
    ns['conversar'] = lambda *args, **kwargs: next(fila)


brutos = {
    24: dict(origem='biblio', destino='cafe mania'),
    25: dict(origem='b4', destino='i5'),
    26: dict(origem='bibliotca', destino='mesa 2'),
    27: dict(origem='cafe manai', destino='easy smrt'),
    28: dict(origem='mesa um', destino='mesa quatro', cenario='lotado'),
    29: dict(origem='ENTRADA PRINCIPAL', destino='patio'),
    30: dict(origem='d1', destino='banheiro fem do design'),
    31: dict(origem='cafe mania', destino='biblioteca'),
    32: dict(origem='mesa 1', destino='mesa 4', cenario='tranqüilo'),
    33: dict(origem='biblioteca', destino='banheiro'),
    34: dict(origem='mesa 1', destino='lanchonete'),
    35: dict(origem='', destino='biblioteca'),
    36: dict(origem='biblioteca', destino='sala 02'),
    37: dict(origem='mesa 1', destino='auditorio'),
    38: dict(origem='biblioteca', destino='B-07'),
    39: dict(origem='biblio', destino='biblio'),
}
for caso in ns['CASOS']:
    nome = 'rota_tempo_previsto' if caso.get('campo_esclarecimento') else caso['ferramenta']
    argumentos = brutos.get(caso['id'], caso['argumentos'])
    respostas_controladas([chamada(nome, argumentos)] if nome else ['Resposta geral.'])
    r = ns['avaliar_caso'](caso)
    assert r['resultado_valido'], (caso['id'], r)
    if caso['ferramenta']:
        assert r['conteudo_automatico'] and r['apresentacao_fiel'], (caso['id'], r)
        assert r['resposta'] == caso['resultado_esperado']
    else:
        assert r['conteudo_automatico'] is None and r['chamadas'] == []
    assert r['resposta_fiel'] is None

# Depois da ferramenta, estes textos nunca devem ser consumidos.
caso = ns['CASOS'][15]
certa = chamada(caso['ferramenta'], caso['argumentos'])
for inventada in ['22,3 segundos são cerca de 3 minutos.', 'Pode ir direto.', '<tool_call>{invalido}']:
    respostas_controladas([certa, inventada])
    d = ns['agente'](caso['pergunta'], mostrar=False, retornar_detalhes=True)
    assert len(d['tentativas']) == 1 and len(d['chamadas']) == 1
    assert d['resposta'] == caso['resultado_esperado'] and inventada not in d['resposta']

invalidas = [
    '<tool_call>{JSON quebrado}</tool_call>',
    '<tool_call>{"name":"rota_tempo_previsto","arguments":{}}',
    certa + certa,
    chamada('ferramenta_do_trio', caso['argumentos']),
    chamada('rota_tempo_previsto', caso['argumentos'] | {'velocidade_kmh': 10}),
    chamada('rota_tempo_previsto', []),
    'Vou recalcular depois.',
]
for invalida in invalidas:
    respostas_controladas([invalida, certa])
    d = ns['agente'](caso['pergunta'], mostrar=False, retornar_detalhes=True)
    assert d['status'] == 'concluido' and len(d['tentativas']) == 2, d
    assert len(d['chamadas']) == 1 and d['resposta'] == caso['resultado_esperado']
respostas_controladas([invalidas[0]] * 3)
d = ns['agente'](caso['pergunta'], mostrar=False, retornar_detalhes=True)
assert d['status'] == 'erro' and not d['chamadas'] and len(d['tentativas']) == 3
assert '<tool_call>' not in d['resposta']

for texto in ['B-07', 'sala 02', 'mesa 5', 'banheiro', 'cafe', 'lanchonete', 'bloco z', 'auditorio', 'Gastro']:
    assert ns['resolver_local'](texto)['local'] is None, texto
for bruto, esperado in [('B4', 'B-04'), ('sala b04', 'B-04'), ('biblio', 'Biblioteca'),
                        ('bibliotca', 'Biblioteca'), ('cafe manai', 'Café Mania'),
                        ('easy smrt', 'Easy Smart'), ('banheiro fem do bloco C', 'WC Feminino C')]:
    assert ns['resolver_local'](bruto)['local'] == esperado, bruto
assert ns['resolver_cenario']('tranqüilo') == 'tranquilo'

# Nome existente escolhido arbitrariamente também deve ser rejeitado.
inventado = dict(name='rota_tempo_previsto', arguments=dict(origem='Mesa 1', destino='WC Feminino Design'))
assert ns['preparar_pedido'](inventado, 'mesa 1 para banheiro')['status'] == 'erro'
inventado['arguments']['destino'] = 'B-06'
assert ns['preparar_pedido'](inventado, 'mesa 1 para B-07')['status'] == 'erro'
assert ns['preparar_pedido'](dict(name='rota_tempo_previsto', arguments=dict(
    origem='Mesa 1', destino='Mesa 4', cenario='movimentado')), 'Mesa 1 até Mesa 4')['status'] == 'erro'

# Continuidade sem nova inferência: responde apenas ao local que faltava.
respostas_controladas([chamada('rota_tempo_previsto', dict(origem='mesa 1', destino='lanchonete'))])
d = ns['agente']('mesa 1 para lanchonete', mostrar=False, retornar_detalhes=True)
assert d['status'] == 'esclarecimento' and not d['chamadas']
pendencia = d['pendencia']
respostas_controladas([])
fim = ns['agente']('Café Mania', mostrar=False, retornar_detalhes=True, pendencia=pendencia)
assert fim['status'] == 'concluido' and fim['chamadas'][0]['pedido']['arguments']['origem'] == 'Mesa 1'
assert fim['chamadas'][0]['pedido']['arguments']['destino'] == 'Café Mania'
assert fim['tentativas'][0]['fonte'] == 'esclarecimento_usuario'
assert fim['tentativas'][0]['resposta_modelo'] is None
cancelado = ns['agente']('cancelar', mostrar=False, retornar_detalhes=True, pendencia=pendencia)
assert cancelado['status'] == 'cancelado' and cancelado['pendencia'] is None

for argumentos, campo, pergunta, resposta in [
    (dict(origem='', destino='Biblioteca'), 'origem', 'quero ir para Biblioteca', 'Cinema'),
    (dict(origem='Mesa 1', destino='Mesa 4', cenario='chuva'), 'cenario', 'Mesa 1 até Mesa 4 na chuva', 'movimentado'),
]:
    respostas_controladas([chamada('rota_tempo_previsto', argumentos)])
    d = ns['agente'](pergunta, mostrar=False, retornar_detalhes=True)
    assert d['pendencia']['campo'] == campo and not d['chamadas']
    respostas_controladas([])
    fim = ns['agente'](resposta, mostrar=False, retornar_detalhes=True, pendencia=d['pendencia'])
    assert fim['status'] == 'concluido', fim

ref = dict(caminho=['Mesa 1', 'Pátio - A', 'Mesa 4'], vizinhos=[], valores=['30.0 s'], sintetico=True)
assert ns['conferir_conteudo']('Mesa 1 → Pátio - A → Mesa 4: 30 segundos. Cenário fictício.', ref)
assert not ns['conferir_conteudo']('Mesa 1 → Pátio - A → Mesa 4: 130 segundos. Sintético.', ref)
assert not ns['conferir_conteudo']('Mesa 4 → Pátio - A → Mesa 1: 30 segundos. Sintético.', ref)
respostas_controladas([])
assert ns['avaliar_caso'](caso)['erro'].startswith('StopIteration')

mensagem = ('OK: 39 referências; testes controlados de aliases/grafia/códigos; ambiguidades e nomes ausentes; '
            'retorno direto sem segunda geração; recuperação limitada de JSON; rejeição de velocidade/argumentos extras; '
            'nomes não citados; esclarecimento com continuidade/cancelamento; regressão em 8100 pares de distância. '
            'Qwen real NÃO executado; não mede interpretação de linguagem natural. Revisão humana e perguntas inéditas pendentes.')
print(mensagem)
(root / 'work/verificacao_interpretacao_v3.txt').write_text(mensagem + '\n', encoding='utf-8')
