# Relatório do Marco 1 — Formulação e Busca

> Rascunho técnico. Antes da entrega, preencher autores e divisão do trabalho, inserir as figuras produzidas pela execução final do notebook e diagramar em PDF com 2 a 4 páginas.

## 1. Problema e representação

O projeto representa o térreo do IESB como um grafo para calcular rotas de um carrinho. Cada local cadastrado é um nó e cada passagem navegável confirmada é uma ligação bidirecional. O grafo atual possui 90 nós e 90 ligações. As ligações usam comprimentos aproximados em metros, documentados em `MAPA_DO_GRAFO.md`; eles ainda não são medições de campo.

O grafo inclui um ciclo no pátio, com dois sentidos possíveis ao redor das mesas. A circulação pelo chão foi confirmada pelo usuário, com ressalva de muitas cadeiras e mesas. As ligações pressupõem espaço disponível e não garantem navegabilidade física no momento da consulta.

## 2. Modelagem em espaço de estados

- Estado: local atual do carrinho, identificado pelo nome de um nó.
- Estado inicial: local escolhido como origem.
- Ações: mover-se para qualquer nó diretamente ligado ao local atual.
- Função de transição: a execução de uma ação troca o estado atual pelo vizinho escolhido.
- Teste de objetivo: o local atual é igual ao destino solicitado.
- Custo de uma ação: comprimento aproximado, em metros, da ligação percorrida.
- Custo do caminho: soma dos comprimentos de todas as ligações percorridas.

Nesta fase, o objetivo é minimizar a distância estimada. O cálculo determinístico de tempo por distância e velocidade constante foi incluído apenas como apoio e não faz parte do custo aprendido exigido na Fase 2.

## 3. Estratégias de busca

A busca de custo uniforme e o A* usam o mesmo laço simples. A fronteira guarda o custo percorrido `g`, o local e o caminho. No custo uniforme, a prioridade é somente `g`. No A*, a prioridade é `f = g + h`.

A heurística adotada é:

`h(local, destino) = |d(Entrada, local) - d(Entrada, destino)|`

As distâncias até a Entrada Principal são calculadas uma vez com custo uniforme. Pela desigualdade triangular, a diferença absoluta entre essas distâncias não supera a menor distância entre o local e o destino. A heurística é, portanto, admissível. A verificação automatizada também confirmou consistência em todas as ligações para os 8.100 pares de origem e destino.

O modelo de linguagem não calcula a rota. Seu papel posterior é interpretar a pergunta e escolher a ferramenta. A busca recebe origem e destino já estruturados e calcula o caminho.

## 4. Experimento comparativo

Foram usados recortes conectados de 20, 40 e 70 nós da mesma planta. Em cada tamanho, a origem foi a Entrada Principal e o destino foi o nó do recorte mais distante dela. Para reduzir picos ocasionais, cada consulta foi executada 30 vezes depois de um aquecimento e foi registrada a mediana do tempo de execução.

| Nós | Destino | Estratégia | Nós expandidos | Custo (m) |
| ---: | --- | --- | ---: | ---: |
| 20 | Eixo - Bloco B | Custo uniforme | 19 | 186 |
| 20 | Eixo - Bloco B | A* | 19 | 186 |
| 40 | Eixo - Fundo | Custo uniforme | 39 | 210 |
| 40 | Eixo - Fundo | A* | 39 | 210 |
| 70 | Corredor Bloco B - 01/04 | Custo uniforme | 69 | 221 |
| 70 | Corredor Bloco B - 01/04 | A* | 69 | 221 |

Os tempos em milissegundos devem ser copiados da execução final usada no relatório, pois variam entre máquinas e sessões. O tempo de preparação da tabela da heurística deve permanecer separado do tempo das consultas.

## 5. Análise dos resultados

As duas estratégias encontraram o mesmo custo ótimo nos três recortes. O A* não reduziu o número de expansões nesta amostra: as contagens foram 19, 39 e 69 para ambas as estratégias. Esse resultado não contradiz a correção da heurística. Admissibilidade e consistência garantem a qualidade da solução, mas não uma vantagem obrigatória de tempo ou de expansões.

A referência única na Entrada Principal produz muitos empates de prioridade. Além disso, há somente uma consulta por tamanho e a topologia possui apenas um ciclo. Por isso, não se pode generalizar que os algoritmos sempre terão o mesmo comportamento. Também não se deve afirmar que o A* foi mais rápido: o laço calcula a heurística e os tempos são muito pequenos e sensíveis ao ambiente.

O enunciado pede pelo menos três mapas de tamanhos diferentes. O experimento atual usa três recortes da mesma planta, não três topologias independentes. Essa escolha controla o crescimento do número de nós, mas é uma limitação que deve ser apresentada com transparência ou corrigida, se o professor exigir mapas distintos.

## 6. Limitações e próximos passos

As distâncias precisam ser conferidas no campus. Portas próximas são agrupadas e as posições das mesas são didáticas. O ciclo do pátio permite comparar rotas em distância e tempo previsto; o cenário de atraso por cadeiras é sintético. Não há percepção de obstáculos ou controle do carrinho. Relatórios finais e validação integral no Colab continuam pendentes.

## 7. Divisão do trabalho

Preencher somente com os nomes e contribuições reais do trio:

| Integrante | Responsabilidade principal | Contribuições realizadas |
| --- | --- | --- |
| Nome 1 | Formulação e busca | A preencher |
| Nome 2 | Dados e aprendizado | A preencher |
| Nome 3 | Agente com LLM e avaliação | A preencher |

