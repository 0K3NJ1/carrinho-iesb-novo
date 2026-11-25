# Análise do código — Carrinho IESB

Análise do notebook `carrinho_iesb_unificado.ipynb` (branch `agente-v5-gabarito`), feita para a videoaula. O código original não foi modificado: as células foram lidas e executadas em cópia, num ambiente separado.

## 1. Estrutura

Um único notebook com células Markdown e de código. Não há classes nem módulos próprios: só funções e variáveis globais compartilhadas entre células. A ordem de execução importa (cada célula usa o que as anteriores criaram).

| célula | seção | linhas |
|---|---|---|
| 2 | 1. Origem e destino | 4 |
| 5 | 2. Mapa e distâncias aproximadas em metros | 112 |
| 7 | 3. A*, custo uniforme e cálculo do tempo | 63 |
| 9 | 4. Referência didática por distância e consulta de vizinhos | 41 |
| 11 | 5. Referência do Marco 1: distância e tempo ideal a 15 km/h | 5 |
| 13 | 5.1 Experimento do Marco 1 — tabela e gráficos | 46 |
| 15 | 5.2 Gráficos | 1 |
| 16 | 5.2 Gráficos | 42 |
| 18 | 5.3 Fase 2 — aprendizado com dados sintéticos | 1 |
| 19 | 5.3 Fase 2 — aprendizado com dados sintéticos | 191 |
| 21 | 6. Qwen do gabarito | 1 |
| 22 | 6. Qwen do gabarito | 41 |
| 24 | 7. O ciclo do agente: pensar → agir → observar → responder | 272 |
| 26 | 8. Perguntas e descrição da ferramenta | 15 |
| 28 | 8.1 Interface opcional por texto | 21 |
| 30 | 8.2 Faça sua pergunta (demonstração ao vivo) | 10 |
| 31 | 8.2 Faça sua pergunta (demonstração ao vivo) | 9 |
| 33 | 9. Avaliação — 39 pedidos de teste | 60 |
| 35 | 9.1 Rodar a avaliação com o Qwen | 58 |
| 39 | 10. Última célula: pergunte ao agente | 8 |

## 2. Bibliotecas

| módulo | nome | tipo | célula |
|---|---|---|---|
| `time` | `perf_counter` | nativa | 7 |
| `statistics` | `median` | nativa | 13 |
| `matplotlib.pyplot` | `plt` | externa | 16 |
| `json` | `json` | nativa | 19 |
| `random` | `random` | nativa | 19 |
| `pathlib` | `Path` | nativa | 19 |
| `numpy` | `np` | externa | 19 |
| `pandas` | `pd` | externa | 19 |
| `sklearn.compose` | `ColumnTransformer` | externa | 19 |
| `sklearn.pipeline` | `make_pipeline` | externa | 19 |
| `sklearn.impute` | `SimpleImputer` | externa | 19 |
| `sklearn.preprocessing` | `OneHotEncoder` | externa | 19 |
| `sklearn.preprocessing` | `StandardScaler` | externa | 19 |
| `sklearn.linear_model` | `LinearRegression` | externa | 19 |
| `sklearn.tree` | `DecisionTreeRegressor` | externa | 19 |
| `sklearn.model_selection` | `GroupKFold` | externa | 19 |
| `sklearn.model_selection` | `GroupShuffleSplit` | externa | 19 |
| `sklearn.model_selection` | `cross_val_predict` | externa | 19 |
| `sklearn.metrics` | `mean_absolute_error` | externa | 19 |
| `sklearn.metrics` | `mean_squared_error` | externa | 19 |
| `sklearn.metrics` | `r2_score` | externa | 19 |
| `torch` | `torch` | externa | 22 |
| `transformers` | `AutoTokenizer` | externa | 22 |
| `transformers` | `AutoModelForCausalLM` | externa | 22 |
| `re` | `re` | nativa | 24 |
| `unicodedata` | `unicodedata` | nativa | 24 |
| `difflib` | `get_close_matches` | nativa | 24 |
| `transformers.utils` | `get_json_schema` | externa | 26 |

Também são usadas as funções nativas `min`, `max`, `abs`, `len`, `sum`, `sorted`, `range`, `enumerate`, `zip`, `isinstance`, `input` e `print`. O projeto **não usa** NetworkX, `heapq`, `math` nem coordenadas.

## 3. Funções

| função | parâmetros | célula · linhas | chama | chamada por | papel |
|---|---|---|---|---|---|
| `h` | local, destino | 7 · 7–10 | — | — (nível da célula) | Heurística como função separada. **Definida, mas não chamada**: `buscar` calcula a mesma fórmula na linha 35. |
| `buscar` | origem, destino, grafo, usar_heuristica, referencia | 7 · 13–38 | — | a_estrela, demonstrar_alternativa_patio, rota_tempo_previsto | Laço único de busca: custo uniforme (`usar_heuristica=False`) ou A* (`True`). Fronteira = lista de tuplas `(f, g, local, caminho)`, escolha com `min`. |
| `a_estrela` | origem, destino | 7 · 41–43 | buscar | calcular_rota, demonstrar_alternativa_patio | Atalho: `buscar` no grafo de metros com heurística; devolve `(caminho, custo)`. |
| `calcular_tempo` | distancia_m, velocidade_kmh | 7 · 56–63 | — | calcular_rota | Converte metros e km/h em segundos (`m × 3,6 ÷ km/h`), validando tipos e valores. |
| `calcular_rota` | origem, destino | 9 · 1–22 | a_estrela, calcular_tempo | — (nível da célula) | Referência do Marco 1: rota de menor distância e tempo ideal sem atrasos. Não é dada ao Qwen. |
| `listar_vizinhos` | local | 9 · 25–37 | — | executar | Ferramenta do agente: lista os vizinhos diretos de um local. |
| `recortar_mapa` | quantidade | 13 · 4–20 | — | — (nível da célula) | Busca em largura a partir da entrada para montar submapas de 20, 40 e 70 nós (experimento). |
| `gerar_dados_sinteticos` | — | 19 · 21–40 | — | — (nível da célula) | Gera 2160 linhas (90 trechos × 2 cenários × 12 repetições) com regra pública e semente 42. |
| `preparar_modelo` | nome | 19 · 48–56 | — | — (nível da célula) | Pipeline: imputação + padronização (numéricas), imputação + one-hot (categóricas), e regressão linear ou árvore. |
| `metricas_tempo` | real, previsto | 19 · 59–62 | — | — (nível da célula) | MAE, RMSE e R² em segundos. |
| `prever_grafo_tempo` | cenario | 19 · 113–132 | — | demonstrar_alternativa_patio, rota_tempo_previsto | Monta o grafo com tempos previstos pelo modelo para um cenário (tranquilo, movimentado, cadeiras no pátio). |
| `rota_tempo_previsto` | origem, destino, cenario | 19 · 135–163 | buscar, prever_grafo_tempo | executar | Ferramenta principal do agente: A* sobre o grafo de tempos, com heurística recalculada em segundos. |
| `demonstrar_alternativa_patio` | — | 19 · 170–185 | a_estrela, buscar, prever_grafo_tempo | — (nível da célula) | Mostra o modelo de custo mudando a rota (Mesa 1 → Mesa 4 com cadeiras no pátio). |
| `conversar` | mensagens, ferramentas, max_tokens | 22 · 23–38 | — | agente | Uma geração do Qwen com `apply_chat_template` (mensagens + ferramentas) e `generate` determinístico. |
| `padronizar` | texto | 24 · 12–25 | — | aparece_na_pergunta, fala_do_mapa, local_na_pergunta, resolver_cenario, resolver_local | Normaliza texto: minúsculas, sem acentos e pontuação, `b4 → b 4`, tabela `TROCAS`, zeros à esquerda. |
| `resolver_local` | texto | 24 · 52–64 | padronizar | local_na_pergunta, preparar_pedido | Texto → local: nome/apelido, genérico (pergunta), número desconhecido (pergunta) ou erro de digitação. |
| `resolver_cenario` | texto | 24 · 67–73 | padronizar | preparar_pedido | Texto → cenário, aceitando sinônimos e grafias próximas (corte 0,7). |
| `aparece_na_pergunta` | textos, pergunta | 24 · 76–78 | padronizar | preparar_pedido | Alguma das palavras aparece na pergunta padronizada? |
| `local_na_pergunta` | local, pergunta | 24 · 81–90 | padronizar, resolver_local | preparar_pedido | O local pedido pelo modelo aparece em algum trecho de 1 a 4 palavras da pergunta? |
| `pergunta_ao_usuario` | campo, opcoes | 24 · 93–97 | — | preparar_pedido | Monta o texto de esclarecimento, com opções quando houver. |
| `preparar_pedido` | pedido, pergunta | 24 · 103–130 | aparece_na_pergunta, local_na_pergunta, pergunta_ao_usuario, resolver_cenario, resolver_local | agente, executar | Confere o pedido do modelo e devolve status `ok`, `erro` ou `esclarecimento`. |
| `executar` | pedido | 24 · 133–141 | listar_vizinhos, preparar_pedido, rota_tempo_previsto | agente | Executa a ferramenta pedida depois de `preparar_pedido`. |
| `fala_do_mapa` | pergunta | 24 · 176–180 | padronizar | agente | A pergunta cita local, nome genérico ou palavra de rota? |
| `extrair_json` | texto | 24 · 183–191 | — | ler_pedido_de_ferramenta | Recorta e converte o JSON do texto do modelo; `None` se inválido. |
| `ler_pedido_de_ferramenta` | resposta | 24 · 194–198 | extrair_json | agente | Lê o pedido de ferramenta (com ou sem as marcas `<tool_call>`). |
| `numeros_fora_da_ferramenta` | resposta, resultados | 24 · 201–208 | — | agente | Controle de alucinação: números da explicação ausentes nos resultados das ferramentas. |
| `agente` | pergunta, mostrar, retornar_detalhes, historico | 24 · 211–271 | conversar, executar, fala_do_mapa, ler_pedido_de_ferramenta, numeros_fora_da_ferramenta, preparar_pedido | conversa_interativa | Ciclo pensar → agir → observar → responder, com até 3 passos. |
| `conversa_interativa` | — | 28 · 1–20 | agente | — (nível da célula) | Chat por texto com `input()`, histórico das duas últimas trocas, `sair` e `cancelar`. |
| `o_que_o_agente_fez` | detalhes | 35 · 5–11 | — | — (nível da célula) | Traduz os detalhes do agente para o formato dos casos de teste. |

## 4. Estruturas de dados principais

- `LOCAIS`: lista de 90 nomes (strings).
- `LIGACOES`: lista de 90 tuplas `(origem, destino, metros)`; o grafo é não direcionado e tem um ciclo (pátio).
- `VIZINHOS`: dicionário `local → [(vizinho, metros), ...]` (lista de adjacência).
- `DISTANCIA_ENTRADA`: dicionário `local → menor distância até a Entrada Principal` (base da heurística).
- Fronteira da busca: lista de tuplas `(f, g, local, caminho)`; `visitados`: lista.
- `DADOS_TEMPO`: DataFrame 2160 × 13; `MODELO_TEMPO`: Pipeline do scikit-learn.
- `REGRAS`: prompt do sistema (versão `VERSAO_REGRAS`); `FERRAMENTAS`: `[rota_tempo_previsto, listar_vizinhos]`.
- `CASOS`: 39 tuplas `(pergunta, o que fazer, argumentos)`.

## 5. Algoritmos

- **Custo uniforme** e **A\***: a mesma função `buscar`. Prioridade `g` ou `g + h`; objetivo testado ao retirar da fronteira; cópias antigas descartadas por `visitados` (`continue`).
- **Heurística**: `h(n) = |d(E, n) − d(E, destino)|`, com E = Entrada Principal; admissível e consistente pela desigualdade triangular. Na Fase 2, a referência é recalculada em segundos no grafo de tempos.
- **Busca em largura** (`recortar_mapa`) para montar os submapas do experimento.
- **Regressão linear** × **árvore de decisão**, com `GroupShuffleSplit` (teste por trecho) e `GroupKFold` (validação cruzada).
- **Agente com ferramentas**: ciclo do gabarito da Aula 10, com conferência dos pedidos e controle de números.

## 6. Fluxo de execução

Constantes (seção 1) → grafo (2) → busca e tabela da heurística (3) → ferramentas da Fase 1 (4) → saídas e experimento (5, 5.1, 5.2) → dados, modelos e custo aprendido (5.3) → carregamento do Qwen (6) → padronização, regras e agente (7) → perguntas e interfaces (8) → avaliação dos 39 casos (9) → `input()` final (10).

## 7. Resultados reais

- Grafo: 90 nós, 90 ligações; tabela da heurística em 3.231 ms (execução local).
- Mesa 1 → Mesa 4: custo uniforme 9 expansões, A* 7, ambos 42 m.
- Experimento (origem = Entrada): expansões iguais (19, 39, 69), custos 186, 210 e 221 m.
- Fase 2: regressão linear escolhida (MAE validação 0.854 s; teste MAE 0.838 s, R² 0.9728).
- Demonstração do pátio: rota muda de A→B (42 m, 35.7 s) para A→D (46 m, 23.7 s).
- Agente (regras v5): 31 de 39 casos certos; 24 de 30 rotas válidas; 4 explicações com número sinalizado. Mediana 3,8 s/pedido (GPU local) e 135 s (Colab sem GPU).

## 8. Erros, limitações e inconsistências encontrados

- `h()` (célula 7) é definida e nunca chamada; a fórmula está repetida dentro de `buscar`.
- No experimento, a origem é o próprio ponto de referência: os nós empatam em `f` e o A* não economiza expansões.
- `rota_tempo_previsto` recalcula a tabela de referência (90 buscas) a cada chamada: correto, mas repetitivo.
- `visitados` é lista e a fronteira usa `min`/`remove`: O(n) por operação (suficiente para 90 nós).
- `recortar_mapa` usa `pop(0)` em lista (O(n)); `collections.deque` seria o padrão para filas.
- `calcular_rota` valida a velocidade chamando `calcular_tempo(0, ...)` dentro de `try`: funciona, mas é indireto.
- A docstring de `listar_vizinhos` diz que “a aplicação normaliza”: a normalização é feita por `preparar_pedido`, não pela função.
- `numeros_fora_da_ferramenta` não detecta caminho reescrito com palavras nem conselhos inventados sem números.
- Dados sintéticos sem faltantes: a imputação existe no Pipeline, mas não é exercitada.
- Não há variável de horário; o agente calcula um destino por vez; os três mapas são recortes do mesmo campus.
- `MAPA_DO_GRAFO.md` (fora do notebook) ainda cita 10 km/h; o notebook usa 15 km/h.
- O Qwen 1.5B acerta 3 de 10 pedidos informais; sem GPU, cada pedido leva cerca de 135 s.
