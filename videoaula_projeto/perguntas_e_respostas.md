# Perguntas e respostas para a defesa

26 perguntas prováveis na arguição cruzada, com respostas baseadas no código real e nas execuções reais. As mesmas aparecem no capítulo 16 da videoaula.

## 1. Por que o projeto usa Python?

Porque é a linguagem da disciplina e do Colab, tem bibliotecas maduras para dados e modelos de linguagem, e permite um código curto e fácil de explicar.

- Linguagem da disciplina e do Colab
- Bibliotecas prontas: scikit-learn, pandas, transformers
- Código curto e legível para a arguição

## 2. Por que `VIZINHOS` é um dicionário?

Porque o algoritmo pergunta o tempo todo quais são os vizinhos de um local, e o dicionário responde direto pela chave. É uma lista de adjacência, ideal para um grafo esparso.

- Acesso direto pela chave: `VIZINHOS[local]`
- Lista de adjacência: guarda só ligações que existem
- Matriz 90 × 90 teria 8100 posições quase vazias

## 3. Por que a busca usa `while` e não `for`?

Porque o número de voltas não é conhecido antes. O laço roda enquanto houver itens na fronteira, e termina com return quando o destino é retirado.

- Não se sabe antes quantas voltas serão necessárias
- Roda enquanto houver itens na fronteira
- Termina com `return` ao achar o destino

## 4. Qual a diferença entre função e método?

Uma função existe sozinha, como min. Um método pertence a um objeto e é chamado com ponto, como fronteira ponto remove. O ponto acessa o que pertence ao objeto.

- Função: existe sozinha, `min(fronteira)`
- Método: pertence a um objeto, `fronteira.remove(melhor)`
- O ponto acessa atributos e métodos do objeto

## 5. Como funciona `pergunta.strip().lower()`?

Strip devolve uma nova string sem os espaços das pontas, e lower age sobre esse resultado, deixando tudo minúsculo. É encadeamento, da esquerda para a direita, e a variável original não muda.

- `strip()` devolve nova string sem espaços nas pontas
- `lower()` age sobre esse resultado: minúsculas
- Encadeamento da esquerda para a direita; `pergunta` não muda

## 6. O que é a fronteira e por que ela é uma lista de tuplas?

É o conjunto de caminhos ainda não explorados. Cada item é uma tupla com f, g, local e caminho, e como o min compara tuplas posição por posição, a lista simples funciona como fila de prioridade.

- Caminhos ainda não explorados
- Tupla `(f, g, local, caminho)`: o `min` compara f, depois g, depois nome
- Lista simples + `min` faz o papel de fila de prioridade

## 7. Qual a diferença entre custo uniforme e A*?

O custo uniforme ordena pela distância já percorrida, g. O A estrela ordena por g mais h. No projeto, é a mesma função buscar, mudando só o parâmetro usar heurística.

- Custo uniforme: prioridade `g(n)`
- A*: prioridade `f(n) = g(n) + h(n)`
- No projeto: a mesma `buscar`, com `usar_heuristica` falso ou verdadeiro

## 8. Como vocês garantem que o caminho é ótimo?

Com três condições: a heurística é admissível e consistente, o objetivo é testado ao retirar o nó da fronteira, e todos os custos são positivos. Os custos do A estrela sempre bateram com os do custo uniforme.

- Heurística admissível e consistente
- Objetivo testado ao **retirar** o nó da fronteira
- Custos positivos; resultados iguais ao custo uniforme

## 9. Qual é a heurística e por que ela é admissível?

É o valor absoluto da diferença entre as distâncias do nó e do destino até a Entrada Principal. Pela desigualdade triangular, essa diferença nunca ultrapassa a distância real entre eles.

- `h(n) = |d(E, n) − d(E, destino)|`, com E = Entrada
- Desigualdade triangular: nunca passa da distância real
- Calculada com busca exata sobre os mesmos pesos

## 10. Por que não usaram distância euclidiana?

Porque o projeto não guarda coordenadas, só nomes e metros. A distância até um ponto de referência dá uma estimativa admissível usando apenas o próprio grafo.

- O projeto não tem coordenadas dos locais
- Só nomes e metros das ligações
- O ponto de referência dá uma estimativa admissível sem coordenadas

## 11. O que acontece se a heurística retornar zero?

Então f é igual a g, e o A estrela vira o custo uniforme. Continua correto, mas perde a direção e pode expandir mais nós.

- `f(n) = g(n)`
- O A* vira exatamente o custo uniforme
- Continua correto, mas sem direção

## 12. Por que, no experimento, o A* expandiu os mesmos nós?

Porque a origem do experimento é a própria Entrada, o ponto de referência. Aí quase todos os nós empatam em f. Com outra origem, como a Mesa 1, o A estrela expandiu 7 nós contra 9.

- A origem é a Entrada, o próprio ponto de referência
- Para os nós alcançados: `f = d(E, destino)`, todos empatam
- De Mesa 1 a Mesa 4: 7 expansões contra 9

## 13. Qual a complexidade da busca do projeto?

A cada volta, min e remove percorrem a fronteira inteira. No pior caso, isso fica na ordem de E ao quadrado. Com heapq e um conjunto de visitados, cairia para E log E.

- `min` e `remove` percorrem a lista: O(tamanho da fronteira) por volta
- Pior caso aproximado: O(E²)
- Com `heapq` e `set`: O(E log E)

## 14. O que aconteceria se o campus fosse muito maior?

A lista com min ficaria lenta, e valeria trocar por heapq e usar um conjunto para os visitados. A tabela da heurística continuaria correta, mas o preparo custaria mais.

- A lista com `min` ficaria lenta: trocar por `heapq`
- `visitados` como `set` em vez de lista
- A tabela da heurística continuaria valendo, mas custa uma busca por local

## 15. Como o modelo de custo foi treinado?

Com 2160 linhas sintéticas geradas por uma regra pública e semente fixa. Um Pipeline faz imputação, padronização e one hot, e a regressão linear venceu a árvore pela menor MAE na validação cruzada por trecho.

- 2160 linhas sintéticas com regra pública e semente 42
- Pipeline: imputação, padronização, one-hot
- Regressão linear × árvore, validação cruzada por trecho, MAE

## 16. Por que separar treino e teste por trecho?

Porque o mesmo trecho no treino e no teste deixaria o teste fácil demais. Agrupando por trecho, medimos se o modelo prevê trechos que nunca viu.

- O mesmo trecho dos dois lados facilitaria demais o teste
- `GroupShuffleSplit` e `GroupKFold` com grupos = trecho
- Mede a capacidade de prever trechos novos

## 17. O que significam MAE, RMSE e R²?

MAE é o erro absoluto médio, 0,84 segundo no teste. RMSE pune mais os erros grandes, 1,16 segundo. E R quadrado é a fração da variação que o modelo explica, 0,97.

- MAE: erro absoluto médio (0,84 s no teste)
- RMSE: pune mais os erros grandes (1,16 s)
- R²: fração da variação explicada (0,97)

## 18. Como o custo aprendido entra no A*?

Prever grafo tempo usa o modelo para trocar os metros por segundos previstos, a referência da heurística é recalculada em segundos, e a mesma função buscar da Fase 1 roda sobre esse grafo.

- `prever_grafo_tempo` monta o grafo com segundos
- Referência da heurística recalculada em segundos
- A mesma `buscar` da Fase 1

## 19. Mostre o modelo de custo mudando a decisão.

Da Mesa 1 até a Mesa 4 com cadeiras no pátio: a rota mais curta, por B, tem 42 metros e 35,7 segundos. O A estrela com tempo escolhe a rota por D, com 46 metros e 23,7 segundos.

- Mesa 1 → Mesa 4 com cadeiras no pátio
- Mais curta (por B): 42 m, 35,7 s
- Mais rápida (por D): 46 m, 23,7 s

## 20. Como o LLM decide qual ferramenta chamar?

Ele lê as regras, a pergunta e a ficha em JSON de cada ferramenta, gerada pela docstring. Então escreve um pedido entre as marcas tool call. Quem executa é o código.

- Lê as regras (system), a pergunta e as fichas JSON das ferramentas
- Escreve um `<tool_call>` com nome e argumentos
- Ele não executa nada: o código executa

## 21. Por que o LLM não calcula a rota?

Porque modelos de linguagem não são confiáveis em cálculos exatos de caminhos. A busca é exata e verificável. O modelo entende o pedido e explica; a ferramenta calcula.

- LLMs são ruins em cálculos exatos de caminhos
- A busca A* é exata e verificável
- O LLM entende e explica; a ferramenta calcula

## 22. Quando o LLM alucina, e o que o código faz?

Na versão 4, ele inventou rotas sem chamar ferramenta; hoje o código pede de novo e, se não conseguir, admite. Locais inventados são recusados, e números fora do resultado são sinalizados.

- Inventou rotas sem ferramenta na v4: hoje o código pede de novo
- Inventou nome: `local_na_pergunta` recusa
- Arredondou número: `numeros_fora_da_ferramenta` sinaliza

## 23. Quanto custa e quanto demora cada chamada?

Não há custo por chamada, porque o modelo roda na sessão, sem chave de API. Mas há tempo: mediana de 3,8 segundos por pedido na GPU e 135 segundos na CPU do Colab.

- Sem API paga e sem chave: o Qwen roda na sessão
- GPU: mediana 3,8 s por pedido
- CPU no Colab: mediana 135 s

## 24. E se o usuário pedir algo fora do escopo?

Se for uma saudação ou pergunta geral, ele responde sem ferramenta, como na capital do Brasil. Se for um local que não existe, como B-07, o programa pede um nome do mapa.

- Saudação ou pergunta geral: responde sem ferramenta
- Local inexistente: pergunta um nome do mapa
- Local genérico: oferece as opções

## 25. Por que existe `preparar_pedido` se o LLM já escolhe os argumentos?

Porque um modelo pequeno erra. Preparar pedido padroniza os nomes e confere tudo antes de executar, devolvendo ok, erro ou esclarecimento. O modelo interpreta, e o código garante.

- O Qwen 1.5B troca nomes, inventa locais e erra cenários
- O código padroniza, confere e decide: ok, erro ou esclarecimento
- O LLM interpreta; o código garante

## 26. Quais são as limitações do projeto?

Os dados são sintéticos, as distâncias são estimativas e não há sensores. O Qwen pequeno acerta só 3 de 10 pedidos informais. E o agente calcula um destino por vez, com experimento em recortes do mesmo mapa.

- Dados sintéticos; distâncias estimadas; sem sensores
- Qwen 1.5B: 3 de 10 em escrita informal
- Um destino por vez; três recortes do mesmo mapa
