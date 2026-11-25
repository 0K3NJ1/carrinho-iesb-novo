"""Dados reais usados pelo roteiro (gerados por ferramentas/tracos.py e pela avaliação no Colab)."""
import csv
import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
T = json.loads((RAIZ / 'dados' / 'tracos.json').read_text(encoding='utf-8'))
D = T['distancia_entrada']


def br(x, casas=1):
    """Número no formato brasileiro (vírgula)."""
    if isinstance(x, float) and x.is_integer() and casas == 0:
        x = int(x)
    texto = f'{x:.{casas}f}' if isinstance(x, float) else str(x)
    return texto.replace('.', ',')


def avaliacao_colab():
    with open(RAIZ / 'dados' / 'colab_zip' / 'avaliacao.csv', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def resumo_colab():
    return json.loads((RAIZ / 'dados' / 'colab_zip' / 'resumo.json').read_text(encoding='utf-8'))


def ambiente_colab():
    return json.loads((RAIZ / 'dados' / 'colab_zip' / 'ambiente.json').read_text(encoding='utf-8'))


def brutos_colab():
    return json.loads((RAIZ / 'dados' / 'colab_zip' / 'erros_respostas_brutas.json').read_text(encoding='utf-8'))


def estados_do_passo(traco, i, destino_final=True):
    """Cores do grafo na iteração i: expandidos, fronteira, nó escolhido e caminho (no fim)."""
    p = traco['passos'][i]
    est = {n: 'expandido' for n in p['visitados']}
    for f in p['fronteira']:
        est.setdefault(f['local'], 'fronteira')
    est[p['escolhido']['local']] = 'atual'
    est[traco['origem']] = est.get(traco['origem'], 'origem') if i else 'atual'
    return est
