"""Calcula exemplos reais das funções de padronização (seção 7), sem carregar o Qwen.

Executa as células do mapa e o início da célula 24 (até `executar`) e grava dados/exemplos_agente.json.
"""
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
nb = json.loads((RAIZ.parent / 'carrinho_iesb_unificado.ipynb').read_text(encoding='utf-8'))
ns = {}
exec(''.join(nb['cells'][5]['source']), ns)
cel24 = ''.join(nb['cells'][24]['source']).split('\n')
fim = next(i for i, l in enumerate(cel24) if l.startswith('# Versões das regras'))
exec('\n'.join(cel24[:fim]), ns)
fonte_resto = '\n'.join(cel24[fim:])
inicio_fala = fonte_resto.index('PALAVRAS_DE_ROTA')
fim_fala = fonte_resto.index('def agente(')
exec(fonte_resto[inicio_fala:fim_fala], ns)

saida = {}
saida['padronizar'] = {t: ns['padronizar'](t) for t in ['Sala B04', 'banheiro fem do Design', 'Café Mania', 'Pátio/Direito',
                                                         'Corredor I/J', 'mesa 01', 'WC Feminino Design', 'B-04']}
saida['resolver_local'] = {t: list(ns['resolver_local'](t)) for t in ['B-04', 'b4', 'biblio', 'bibliotca', 'cafe manai', 'banheiro',
                                                                       'lanchonete', 'sala 02', 'B-07', 'auditorio', '']}
saida['resolver_cenario'] = {t: ns['resolver_cenario'](t) for t in ['lotado', 'tranqüilo', 'tranqulho', 'tranq', 'cadeiras', 'chuva']}
saida['local_na_pergunta'] = {
    'Café Mania em "cafe manai para easy smrt"': ns['local_na_pergunta']('Café Mania', 'cafe manai para easy smrt'),
    'Mesa 3 em "da biblioteca para o banheiro"': ns['local_na_pergunta']('Mesa 3', 'da biblioteca para o banheiro'),
}
pedidos = [
    ({'name': 'rota_tempo_previsto', 'arguments': {'origem': 'biblio', 'destino': 'b4'}}, 'biblio para b4'),
    ({'name': 'rota_tempo_previsto', 'arguments': {'origem': 'Biblioteca', 'destino': 'banheiro'}}, 'da biblioteca para o banheiro'),
    ({'name': 'rota_tempo_previsto', 'arguments': {'origem': 'Biblioteca', 'destino': 'Mesa 3'}}, 'inventa local'),
    ({'name': 'rota_tempo_previsto', 'arguments': {'origem': 'Mesa 1', 'destino': 'Mesa 4', 'velocidade': 10}}, 'mesa 1 ate mesa 4'),
    ({'name': 'rota_tempo_previsto', 'arguments': {'origem': 'Mesa 1', 'destino': 'Mesa 4', 'cenario': 'movimentado'}},
     'Da Mesa 1 até a Mesa 4, considere cadeiras no pátio.'),
    ({'name': 'voar', 'arguments': {}}, 'quero voar'),
]
saida['preparar_pedido'] = [dict(pedido=p, pergunta=q, resultado=ns['preparar_pedido'](p, q)) for p, q in pedidos]
saida['fala_do_mapa'] = {t: ns['fala_do_mapa'](t) for t in ['Bom dia!', 'Qual é a capital do Brasil?', 'mesa 1 pra lanchonete', 'cafe manai para easy smrt']}
saida['extrair_json'] = ns['extrair_json']('<tool_call>\n{"name": "listar_vizinhos", "arguments": {"local": "Cinema"}}\n</tool_call>')
saida['numeros_fora'] = ns['numeros_fora_da_ferramenta'](
    'A rota leva aproximadamente 74 segundos.\n1. Mesa 1\n2. Pátio - A',
    ['Caminho: Mesa 1 -> Pátio - A -> Pátio - B -> Pátio/Direito -> Mesa 4\nDistância aproximada desta rota: 42.0 m.\nTempo previsto com atrasos: 74.2 s.'])
saida['nomes_total'] = len(ns['NOMES'])
(RAIZ / 'dados' / 'exemplos_agente.json').write_text(json.dumps(saida, ensure_ascii=False, indent=1), encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')
print(json.dumps(saida, ensure_ascii=False, indent=1))
