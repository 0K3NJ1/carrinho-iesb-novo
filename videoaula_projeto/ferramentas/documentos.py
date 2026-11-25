"""Gera analise_codigo.md e perguntas_e_respostas.md a partir do inventário, dos dados reais e do roteiro."""
import importlib.util
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / 'roteiro'))


def carregar(nome):
    spec = importlib.util.spec_from_file_location(nome, RAIZ / 'roteiro' / f'{nome}.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


NATIVOS = {'time', 'statistics', 'json', 'random', 'pathlib', 're', 'unicodedata', 'difflib'}
PAPEL = {
    'h': 'Heurística como função separada. **Definida, mas não chamada**: `buscar` calcula a mesma fórmula na linha 35.',
    'buscar': 'Laço único de busca: custo uniforme (`usar_heuristica=False`) ou A* (`True`). Fronteira = lista de tuplas `(f, g, local, caminho)`, escolha com `min`.',
    'a_estrela': 'Atalho: `buscar` no grafo de metros com heurística; devolve `(caminho, custo)`.',
    'calcular_tempo': 'Converte metros e km/h em segundos (`m × 3,6 ÷ km/h`), validando tipos e valores.',
    'calcular_rota': 'Referência do Marco 1: rota de menor distância e tempo ideal sem atrasos. Não é dada ao Qwen.',
    'listar_vizinhos': 'Ferramenta do agente: lista os vizinhos diretos de um local.',
    'recortar_mapa': 'Busca em largura a partir da entrada para montar submapas de 20, 40 e 70 nós (experimento).',
    'gerar_dados_sinteticos': 'Gera 2160 linhas (90 trechos × 2 cenários × 12 repetições) com regra pública e semente 42.',
    'preparar_modelo': 'Pipeline: imputação + padronização (numéricas), imputação + one-hot (categóricas), e regressão linear ou árvore.',
    'metricas_tempo': 'MAE, RMSE e R² em segundos.',
    'prever_grafo_tempo': 'Monta o grafo com tempos previstos pelo modelo para um cenário (tranquilo, movimentado, cadeiras no pátio).',
    'rota_tempo_previsto': 'Ferramenta principal do agente: A* sobre o grafo de tempos, com heurística recalculada em segundos.',
    'demonstrar_alternativa_patio': 'Mostra o modelo de custo mudando a rota (Mesa 1 → Mesa 4 com cadeiras no pátio).',
    'conversar': 'Uma geração do Qwen com `apply_chat_template` (mensagens + ferramentas) e `generate` determinístico.',
    'padronizar': 'Normaliza texto: minúsculas, sem acentos e pontuação, `b4 → b 4`, tabela `TROCAS`, zeros à esquerda.',
    'resolver_local': 'Texto → local: nome/apelido, genérico (pergunta), número desconhecido (pergunta) ou erro de digitação.',
    'resolver_cenario': 'Texto → cenário, aceitando sinônimos e grafias próximas (corte 0,7).',
    'aparece_na_pergunta': 'Alguma das palavras aparece na pergunta padronizada?',
    'local_na_pergunta': 'O local pedido pelo modelo aparece em algum trecho de 1 a 4 palavras da pergunta?',
    'pergunta_ao_usuario': 'Monta o texto de esclarecimento, com opções quando houver.',
    'preparar_pedido': 'Confere o pedido do modelo e devolve status `ok`, `erro` ou `esclarecimento`.',
    'executar': 'Executa a ferramenta pedida depois de `preparar_pedido`.',
    'fala_do_mapa': 'A pergunta cita local, nome genérico ou palavra de rota?',
    'extrair_json': 'Recorta e converte o JSON do texto do modelo; `None` se inválido.',
    'ler_pedido_de_ferramenta': 'Lê o pedido de ferramenta (com ou sem as marcas `<tool_call>`).',
    'numeros_fora_da_ferramenta': 'Controle de alucinação: números da explicação ausentes nos resultados das ferramentas.',
    'agente': 'Ciclo pensar → agir → observar → responder, com até 3 passos.',
    'conversa_interativa': 'Chat por texto com `input()`, histórico das duas últimas trocas, `sair` e `cancelar`.',
    'o_que_o_agente_fez': 'Traduz os detalhes do agente para o formato dos casos de teste.',
}


def analise():
    inv = json.loads((RAIZ / 'dados' / 'inventario.json').read_text(encoding='utf-8'))
    cod = json.loads((RAIZ / 'dados' / 'codigo.json').read_text(encoding='utf-8'))
    tr = json.loads((RAIZ / 'dados' / 'tracos.json').read_text(encoding='utf-8'))
    resumo = json.loads((RAIZ / 'dados' / 'colab_zip' / 'resumo.json').read_text(encoding='utf-8'))
    L = ['# Análise do código — Carrinho IESB', '',
         'Análise do notebook `carrinho_iesb_unificado.ipynb` (branch `agente-v5-gabarito`), feita para a videoaula. '
         'O código original não foi modificado: as células foram lidas e executadas em cópia, num ambiente separado.', '',
         '## 1. Estrutura', '',
         'Um único notebook com células Markdown e de código. Não há classes nem módulos próprios: só funções e variáveis '
         'globais compartilhadas entre células. A ordem de execução importa (cada célula usa o que as anteriores criaram).', '',
         '| célula | seção | linhas |', '|---|---|---|']
    L += [f"| {k} | {v['titulo']} | {len(v['texto'])} |" for k, v in cod.items()]
    L += ['', '## 2. Bibliotecas', '', '| módulo | nome | tipo | célula |', '|---|---|---|---|']
    vistos = set()
    for i in inv['importacoes']:
        k = (i['modulo'], i['nome'])
        if k in vistos:
            continue
        vistos.add(k)
        raiz = (i['modulo'] or '').split('.')[0]
        L.append(f"| `{i['modulo']}` | `{i['nome']}` | {'nativa' if raiz in NATIVOS else 'externa'} | {i['celula']} |")
    L += ['', 'Também são usadas as funções nativas `min`, `max`, `abs`, `len`, `sum`, `sorted`, `range`, `enumerate`, `zip`, '
          '`isinstance`, `input` e `print`. O projeto **não usa** NetworkX, `heapq`, `math` nem coordenadas.', '',
          '## 3. Funções', '', '| função | parâmetros | célula · linhas | chama | chamada por | papel |', '|---|---|---|---|---|---|']
    for f in inv['funcoes']:
        L.append(f"| `{f['nome']}` | {', '.join(f['parametros']) or '—'} | {f['celula']} · {f['linha_inicio']}–{f['linha_fim']} | "
                 f"{', '.join(f['chama_do_projeto']) or '—'} | {', '.join(f['chamada_por']) or '— (nível da célula)'} | {PAPEL.get(f['nome'], '')} |")
    L += ['', '## 4. Estruturas de dados principais', '',
          '- `LOCAIS`: lista de 90 nomes (strings).',
          '- `LIGACOES`: lista de 90 tuplas `(origem, destino, metros)`; o grafo é não direcionado e tem um ciclo (pátio).',
          '- `VIZINHOS`: dicionário `local → [(vizinho, metros), ...]` (lista de adjacência).',
          '- `DISTANCIA_ENTRADA`: dicionário `local → menor distância até a Entrada Principal` (base da heurística).',
          '- Fronteira da busca: lista de tuplas `(f, g, local, caminho)`; `visitados`: lista.',
          '- `DADOS_TEMPO`: DataFrame 2160 × 13; `MODELO_TEMPO`: Pipeline do scikit-learn.',
          '- `REGRAS`: prompt do sistema (versão `VERSAO_REGRAS`); `FERRAMENTAS`: `[rota_tempo_previsto, listar_vizinhos]`.',
          '- `CASOS`: 39 tuplas `(pergunta, o que fazer, argumentos)`.', '',
          '## 5. Algoritmos', '',
          '- **Custo uniforme** e **A\\***: a mesma função `buscar`. Prioridade `g` ou `g + h`; objetivo testado ao retirar da fronteira; '
          'cópias antigas descartadas por `visitados` (`continue`).',
          '- **Heurística**: `h(n) = |d(E, n) − d(E, destino)|`, com E = Entrada Principal; admissível e consistente pela desigualdade triangular. '
          'Na Fase 2, a referência é recalculada em segundos no grafo de tempos.',
          '- **Busca em largura** (`recortar_mapa`) para montar os submapas do experimento.',
          '- **Regressão linear** × **árvore de decisão**, com `GroupShuffleSplit` (teste por trecho) e `GroupKFold` (validação cruzada).',
          '- **Agente com ferramentas**: ciclo do gabarito da Aula 10, com conferência dos pedidos e controle de números.', '',
          '## 6. Fluxo de execução', '',
          'Constantes (seção 1) → grafo (2) → busca e tabela da heurística (3) → ferramentas da Fase 1 (4) → saídas e experimento (5, 5.1, 5.2) '
          '→ dados, modelos e custo aprendido (5.3) → carregamento do Qwen (6) → padronização, regras e agente (7) → perguntas e interfaces (8) '
          '→ avaliação dos 39 casos (9) → `input()` final (10).', '',
          '## 7. Resultados reais', '',
          f"- Grafo: {len(tr['locais'])} nós, {len(tr['ligacoes'])} ligações; tabela da heurística em {tr['tempo_preparo_ms']} ms (execução local).",
          f"- Mesa 1 → Mesa 4: custo uniforme {tr['ucs_mesa1_mesa4']['expandidos']} expansões, A* {tr['astar_mesa1_mesa4']['expandidos']}, ambos 42 m.",
          '- Experimento (origem = Entrada): expansões iguais (19, 39, 69), custos 186, 210 e 221 m.',
          f"- Fase 2: regressão linear escolhida (MAE validação {tr['validacao'][0]['mae_s']:.3f} s; teste MAE {tr['teste']['mae_s']:.3f} s, R² {tr['teste']['r2']:.4f}).",
          f"- Demonstração do pátio: rota muda de A→B (42 m, {tr['demonstracao_patio']['tempo_rota_curta_s']:.1f} s) para A→D "
          f"({tr['demonstracao_patio']['distancia_rota_tempo_m']} m, {tr['demonstracao_patio']['tempo_previsto_s']:.1f} s).",
          f"- Agente (regras v5): {resumo['fase3']['escolha_certa']} de {resumo['fase3']['casos']} casos certos; "
          f"{resumo['fase3']['rotas_validas']} de {resumo['fase3']['total_rotas']} rotas válidas; "
          f"{resumo['fase3']['com_numero_inventado']} explicações com número sinalizado. Mediana 3,8 s/pedido (GPU local) e "
          f"{resumo['fase3']['mediana_s']:.0f} s (Colab sem GPU).", '',
          '## 8. Erros, limitações e inconsistências encontrados', '',
          '- `h()` (célula 7) é definida e nunca chamada; a fórmula está repetida dentro de `buscar`.',
          '- No experimento, a origem é o próprio ponto de referência: os nós empatam em `f` e o A* não economiza expansões.',
          '- `rota_tempo_previsto` recalcula a tabela de referência (90 buscas) a cada chamada: correto, mas repetitivo.',
          '- `visitados` é lista e a fronteira usa `min`/`remove`: O(n) por operação (suficiente para 90 nós).',
          '- `recortar_mapa` usa `pop(0)` em lista (O(n)); `collections.deque` seria o padrão para filas.',
          '- `calcular_rota` valida a velocidade chamando `calcular_tempo(0, ...)` dentro de `try`: funciona, mas é indireto.',
          '- A docstring de `listar_vizinhos` diz que “a aplicação normaliza”: a normalização é feita por `preparar_pedido`, não pela função.',
          '- `numeros_fora_da_ferramenta` não detecta caminho reescrito com palavras nem conselhos inventados sem números.',
          '- Dados sintéticos sem faltantes: a imputação existe no Pipeline, mas não é exercitada.',
          '- Não há variável de horário; o agente calcula um destino por vez; os três mapas são recortes do mesmo campus.',
          '- `MAPA_DO_GRAFO.md` (fora do notebook) ainda cita 10 km/h; o notebook usa 15 km/h.',
          '- O Qwen 1.5B acerta 3 de 10 pedidos informais; sem GPU, cada pedido leva cerca de 135 s.']
    (RAIZ / 'analise_codigo.md').write_text('\n'.join(L) + '\n', encoding='utf-8')


def perguntas():
    qa = carregar('cap16_defesa').QA
    L = ['# Perguntas e respostas para a defesa', '',
         f'{len(qa)} perguntas prováveis na arguição cruzada, com respostas baseadas no código real e nas execuções reais. '
         'As mesmas aparecem no capítulo 16 da videoaula.', '']
    for i, (q, itens, fala) in enumerate(qa, start=1):
        L += [f'## {i}. {q}', '', fala, ''] + [f'- {x}' for x in itens] + ['']
    (RAIZ / 'perguntas_e_respostas.md').write_text('\n'.join(L), encoding='utf-8')


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    analise()
    perguntas()
    print('analise_codigo.md e perguntas_e_respostas.md gerados')
