# FASE_2_SINTETICA: executada também dentro do notebook unificado.
import json
import random
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import GroupKFold, GroupShuffleSplit, cross_val_predict
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

SEMENTE_DADOS = 42
PASTA_FASE2 = Path('resultados_fase2_15kmh')
PASTA_FASE2.mkdir(exist_ok=True)


def gerar_dados_sinteticos():
    sorteio = random.Random(SEMENTE_DADOS)
    linhas = []
    for trecho, (origem, destino, distancia) in enumerate(LIGACOES):
        # Atributos fictícios: não descrevem portas/pisos observados no campus.
        piso = sorteio.choice(['regular', 'irregular'])
        porta = sorteio.choice([0, 1])
        for cenario in ['tranquilo', 'movimentado']:
            for repeticao in range(12):
                fluxo = sorteio.randint(0, 2) if cenario == 'tranquilo' else sorteio.randint(3, 5)
                obstaculo = int(sorteio.random() < (0.1 if cenario == 'tranquilo' else 0.4))
                base = distancia * 3.6 / VELOCIDADE_BASE_KMH
                tempo = (base * (1 + 0.15 * fluxo + 0.25 * (piso == 'irregular'))
                         + 3 * porta + 12 * obstaculo + sorteio.gauss(0, 0.8))
                linhas.append(dict(trecho=trecho, origem=origem, destino=destino,
                                   distancia_m=distancia, cenario=cenario, fluxo=fluxo,
                                   piso=piso, porta=porta, obstaculo=obstaculo,
                                   repeticao=repeticao, tempo_s=max(0.1, tempo),
                                   origem_do_dado='sintetico', velocidade_base_kmh=VELOCIDADE_BASE_KMH))
    return pd.DataFrame(linhas)


NUMERICAS = ['distancia_m', 'fluxo', 'porta', 'obstaculo']
CATEGORICAS = ['piso', 'cenario']
ENTRADAS = NUMERICAS + CATEGORICAS


def preparar_modelo(nome):
    numericas = make_pipeline(SimpleImputer(strategy='median'), StandardScaler())
    categorias = make_pipeline(SimpleImputer(strategy='most_frequent'),
                               OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    preparo = ColumnTransformer([('numericas', numericas, NUMERICAS),
                                 ('categorias', categorias, CATEGORICAS)])
    estimador = LinearRegression() if nome == 'regressao_linear' else DecisionTreeRegressor(
        max_depth=8, min_samples_leaf=5, random_state=SEMENTE_DADOS)
    return make_pipeline(preparo, estimador)


def metricas_tempo(real, previsto):
    return dict(mae_s=float(mean_absolute_error(real, previsto)),
                rmse_s=float(np.sqrt(mean_squared_error(real, previsto))),
                r2=float(r2_score(real, previsto)))


DADOS_TEMPO = gerar_dados_sinteticos()
# Não há faltantes ou descartes na geração. A imputação é aprendida dentro de cada fold.
assert not DADOS_TEMPO.isna().any().any()
assert not DADOS_TEMPO.duplicated(['trecho', 'cenario', 'repeticao']).any()
assert (DADOS_TEMPO.tempo_s > 0).all()
DADOS_TEMPO.to_csv(PASTA_FASE2 / 'tempos_sinteticos.csv', index=False)

separador = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=SEMENTE_DADOS)
indices_treino, indices_teste = next(separador.split(DADOS_TEMPO, groups=DADOS_TEMPO.trecho))
treino = DADOS_TEMPO.iloc[indices_treino]
teste = DADOS_TEMPO.iloc[indices_teste]
assert set(treino.trecho).isdisjoint(teste.trecho)
COMPARACAO_MODELOS = []
for nome in ['regressao_linear', 'arvore_decisao']:
    previsto = cross_val_predict(preparar_modelo(nome), treino[ENTRADAS], treino.tempo_s,
                                 groups=treino.trecho, cv=GroupKFold(n_splits=5))
    previsto = np.maximum(0.1, previsto)
    COMPARACAO_MODELOS.append(dict(modelo=nome, **metricas_tempo(treino.tempo_s, previsto)))
MELHOR_MODELO = min(COMPARACAO_MODELOS, key=lambda r: r['mae_s'])['modelo']
modelo_avaliado = preparar_modelo(MELHOR_MODELO)
modelo_avaliado.fit(treino[ENTRADAS], treino.tempo_s)
previsoes_teste = np.maximum(0.1, modelo_avaliado.predict(teste[ENTRADAS]))
METRICAS_TESTE = metricas_tempo(teste.tempo_s, previsoes_teste)
erros = teste.copy()
erros['previsto_s'] = previsoes_teste
erros['erro_absoluto_s'] = abs(erros.tempo_s - erros.previsto_s)
erros.to_csv(PASTA_FASE2 / 'previsoes_teste.csv', index=False)
pd.DataFrame(COMPARACAO_MODELOS).to_csv(PASTA_FASE2 / 'validacao_cruzada.csv', index=False)
print('Dados SINTÉTICOS:', len(DADOS_TEMPO), 'linhas;', len(LIGACOES), 'trechos; 24 cenários/repetições por trecho.')
print('Validação cruzada por trecho (5 folds), apenas no treino:')
print(pd.DataFrame(COMPARACAO_MODELOS).to_string(index=False))
print('Escolhido pelo menor MAE de validação:', MELHOR_MODELO)
print('Teste reservado por trecho, usado somente depois da escolha:', METRICAS_TESTE)
print('Erro médio absoluto por cenário no teste:')
print(erros.groupby('cenario').erro_absoluto_s.mean())
print('Cinco maiores erros no teste:')
print(erros.nlargest(5, 'erro_absoluto_s')[['origem', 'destino', 'cenario', 'tempo_s', 'previsto_s', 'erro_absoluto_s']].to_string(index=False))
(PASTA_FASE2 / 'resumo.json').write_text(json.dumps(dict(
    semente=SEMENTE_DADOS, velocidade_base_kmh=VELOCIDADE_BASE_KMH,
    custo_rota='tempo_previsto_s', linhas=len(DADOS_TEMPO), trechos_treino=sorted(treino.trecho.unique().tolist()),
    trechos_teste=sorted(teste.trecho.unique().tolist()), validacao=COMPARACAO_MODELOS,
    escolhido=MELHOR_MODELO, teste=METRICAS_TESTE), ensure_ascii=False, indent=2))

# Reajuste final para uso da ferramenta. As métricas acima são anteriores a esse reajuste.
MODELO_TEMPO = preparar_modelo(MELHOR_MODELO)
MODELO_TEMPO.fit(DADOS_TEMPO[ENTRADAS], DADOS_TEMPO.tempo_s)


def prever_grafo_tempo(cenario):
    if cenario not in ['tranquilo', 'movimentado', 'cadeiras_no_patio']:
        raise ValueError('Cenário desconhecido.')
    atributos = DADOS_TEMPO.drop_duplicates('trecho')[ENTRADAS].reset_index(drop=True).copy()
    base = 'tranquilo' if cenario == 'cadeiras_no_patio' else cenario
    atributos['cenario'] = base
    atributos['fluxo'] = 1 if base == 'tranquilo' else 4
    atributos['obstaculo'] = 0 if base == 'tranquilo' else 1
    if cenario == 'cadeiras_no_patio':
        # Cenário didático: atraso no trecho A-B, sem alegar bloqueio real detectado.
        for indice, (origem, destino, _) in enumerate(LIGACOES):
            if {origem, destino} == {'Pátio - A', 'Pátio - B'}:
                atributos.loc[indice, ['cenario', 'fluxo', 'obstaculo']] = ['movimentado', 5, 1]
    tempos = np.maximum(0.1, MODELO_TEMPO.predict(atributos))
    assert len(tempos) == len(LIGACOES)
    grafo = {local: [] for local in LOCAIS}
    for (origem, destino, distancia), segundos in zip(LIGACOES, tempos):
        grafo[origem].append((destino, float(segundos)))
        grafo[destino].append((origem, float(segundos)))
    return grafo


def rota_tempo_previsto(origem: str, destino: str, cenario: str = 'tranquilo') -> str:
    """Consulta caminho, distância e menor tempo previsto, com base fixa de 15 km/h.

    Use para todos os pedidos de rota, distância e tempo. Os atrasos são sintéticos.
    Não recebe velocidade: 15 km/h é a base fixa da simulação, não a média da viagem.

    Args:
        origem: local de partida como escrito pelo usuário; a aplicação normaliza antes de executar
        destino: local de chegada como escrito pelo usuário; a aplicação normaliza antes de executar
        cenario: cenário fictício; omitir para tranquilo (choices: ["tranquilo", "movimentado", "cadeiras_no_patio"])
    """
    if origem not in LOCAIS or destino not in LOCAIS:
        return 'Erro: origem ou destino não existe no mapa.'
    if cenario not in ['tranquilo', 'movimentado', 'cadeiras_no_patio']:
        return 'Erro: cenário deve ser tranquilo, movimentado ou cadeiras_no_patio.'
    grafo = prever_grafo_tempo(cenario)
    # Referência em SEGUNDOS: nunca reutilizar a heurística antiga em metros.
    referencia = {local: buscar('Entrada Principal', local, grafo, False)[1] for local in LOCAIS}
    caminho, segundos, expandidos = buscar(origem, destino, grafo, True, referencia)
    if caminho is None:
        return 'Não existe caminho entre os locais.'
    distancia = sum(dict(VIZINHOS[a])[b] for a, b in zip(caminho, caminho[1:]))
    aviso = 'Origem e destino coincidem; não há deslocamento no grafo.\n' if origem == destino else ''
    return (aviso + 'Caminho: ' + ' -> '.join(caminho)
            + f'\nDistância aproximada desta rota: {distancia:.1f} m.'
            + f'\nTempo previsto com atrasos: {segundos:.1f} s.'
            + f'\nVelocidade base fixa: {VELOCIDADE_BASE_KMH:g} km/h.'
            + '\nCenário SINTÉTICO: ' + cenario + '. Modelo: ' + MELHOR_MODELO
            + '.\nSem validação de tempo no campus; conferir passagem entre móveis.')


for cenario in ['tranquilo', 'movimentado']:
    print(rota_tempo_previsto(ORIGEM, DESTINO, cenario))


def demonstrar_alternativa_patio():
    origem, destino = 'Mesa 1', 'Mesa 4'
    curto, metros = a_estrela(origem, destino)
    grafo = prever_grafo_tempo('cadeiras_no_patio')
    referencia = {local: buscar('Entrada Principal', local, grafo, False)[1] for local in LOCAIS}
    rapido, tempo, _ = buscar(origem, destino, grafo, True, referencia)
    tempo_curto = sum(dict(grafo[a])[b] for a, b in zip(curto, curto[1:]))
    metros_rapido = sum(dict(VIZINHOS[a])[b] for a, b in zip(rapido, rapido[1:]))
    resultado = dict(origem=origem, destino=destino, cenario='cadeiras_no_patio',
                     velocidade_base_kmh=VELOCIDADE_BASE_KMH,
                     rota_distancia=curto, distancia_m=metros, tempo_rota_curta_s=tempo_curto,
                     rota_tempo=rapido, distancia_rota_tempo_m=metros_rapido, tempo_previsto_s=tempo,
                     mudou=curto != rapido, economia_prevista_s=tempo_curto - tempo)
    print('Demonstração SINTÉTICA; requer passagem física disponível:', resultado)
    (PASTA_FASE2 / 'demonstracao_patio.json').write_text(json.dumps(resultado, ensure_ascii=False, indent=2))
    return resultado


DEMONSTRACAO_PATIO = demonstrar_alternativa_patio()
