# Roteiro completo da videoaula

## Capítulo 1 — Abertura: o que vamos aprender  (início 00:00:00, duração 00:02:46)

**[00:00:00] Bloco 1** · _titulo: O carrinho do IESB, linha por linha_  
Olá! Nesta videoaula você vai entender, linha por linha, o código do projeto de Inteligência Artificial do carrinho do IESB. O objetivo não é só apresentar o projeto: é aprender a ler, explicar e defender cada parte do código.

**[00:00:15] Bloco 2** · _topicos: O problema_  
Primeiro, o problema. Um carrinho precisa ir de um local do térreo do IESB até outro, por exemplo da Biblioteca até uma mesa do pátio.

**[00:00:24] Bloco 3** · _topicos: O problema_  
Para o computador resolver isso, o campus é transformado num grafo: cada local é um nó e cada passagem entre dois locais é uma ligação com um custo.

**[00:00:33] Bloco 4** · _topicos: O problema_  
E a pergunta que o agente responde é sempre a mesma: qual é a melhor rota? O que muda ao longo do projeto é o significado de “melhor”.

**[00:00:42] Bloco 5** · _fluxo: As três fases num só agente_  
O enunciado divide o projeto em três fases, e o código do notebook reúne as três numa peça só. Vamos olhar o desenho geral antes dos detalhes.

**[00:00:52] Bloco 6** · _fluxo: As três fases num só agente_  
Na Fase 1, o agente é ingênuo: conhece só o mapa e as distâncias em metros. A função `buscar` encontra a rota de menor distância com o algoritmo A estrela.

**[00:01:03] Bloco 7** · _fluxo: As três fases num só agente_  
Na Fase 2, entram os obstáculos: fluxo de pessoas, piso irregular, portas e obstáculos. Um modelo de regressão aprende, com dados, quanto tempo cada trecho leva.

**[00:01:14] Bloco 8** · _fluxo: As três fases num só agente_  
A mesma busca da Fase 1 continua rodando, mas agora o custo de cada ligação é o tempo previsto pelo modelo, e não mais a distância.

**[00:01:22] Bloco 9** · _fluxo: As três fases num só agente_  
Na Fase 3, um modelo de linguagem, o Qwen, recebe a pergunta em português, decide qual ferramenta chamar e explica o resultado. Ele não calcula a rota: quem calcula é a busca.

**[00:01:35] Bloco 10** · _fluxo: As três fases num só agente_  
Esta é a ideia central do projeto: nada é jogado fora. O agente final contém as três fases funcionando juntas.

**[00:01:44] Bloco 11** · _topicos: Como a aula está organizada_  
A aula está dividida em capítulos independentes. Primeiro, o notebook e a linguagem Python. Depois, o grafo, a busca, a heurística e o A estrela.

**[00:01:55] Bloco 12** · _topicos: Como a aula está organizada_  
Em seguida, a Fase 2, com os dados e os modelos, e a Fase 3, com o Qwen e o ciclo do agente.

**[00:02:03] Bloco 13** · _topicos: Como a aula está organizada_  
No final, os resultados reais da avaliação, uma simulação completa do programa e um capítulo só com perguntas que o professor pode fazer na arguição.

**[00:02:12] Bloco 14** · _topicos: Antes de começar_  
Um aviso importante para a defesa. Tudo o que aparece aqui vem do código real e de execuções reais. Quando eu mostrar um exemplo que não é do projeto, o painel avisa.

**[00:02:23] Bloco 15** · _topicos: Antes de começar_  
E saiba o que o projeto não usa. Não há NetworkX, não há `heapq`, não há coordenadas nem distância euclidiana. A heurística é outra, e vamos ver qual.

**[00:02:34] Bloco 16** · _topicos: Antes de começar_  
Também não há classes, então não existe `self` no código. Tudo é feito com funções, listas, tuplas e dicionários, como no gabarito do professor. Vamos começar.

## Capítulo 2 — O notebook por dentro e as bibliotecas  (início 00:02:46, duração 00:04:04)

**[00:02:46] Bloco 1** · _titulo: O notebook por dentro_  
Capítulo dois. Antes de olhar algoritmos, vamos entender onde o código mora e em que ordem ele roda.

**[00:02:53] Bloco 2** · _topicos: O que é um notebook_  
O projeto é um único arquivo: `carrinho_iesb_unificado.ipynb`. Um notebook é uma sequência de células. Algumas são de texto, em Markdown, e outras são de código Python.

**[00:03:06] Bloco 3** · _topicos: O que é um notebook_  
Quando uma célula de código roda, as variáveis e funções que ela cria ficam guardadas na memória da sessão. Por isso a ordem importa.

**[00:03:15] Bloco 4** · _topicos: O que é um notebook_  
A célula do agente, por exemplo, usa `LOCAIS`, `buscar` e `rota_tempo_previsto`, que foram criados lá atrás. Se você pular células, aparece um erro de nome não definido.

**[00:03:27] Bloco 5** · _fluxo: A ordem de execução do notebook_  
Este é o caminho que o “Executar tudo” percorre. Cada caixa é uma seção do notebook, e cada seção depende das anteriores.

**[00:03:35] Bloco 6** · _fluxo: A ordem de execução do notebook_  
Primeiro vêm as constantes, o mapa e a busca. Esta é a Fase 1.

**[00:03:41] Bloco 7** · _fluxo: A ordem de execução do notebook_  
Depois, a Fase 2 gera os dados e treina o modelo de tempo.

**[00:03:46] Bloco 8** · _fluxo: A ordem de execução do notebook_  
Em seguida, a Fase 3 carrega o Qwen, define o agente, faz perguntas, roda a avaliação e termina com uma célula que espera você digitar.

**[00:03:55] Bloco 9** · _código: célula 2, linhas 1–3_  
Vamos ler a primeira célula de código. São três linhas, e cada uma é uma atribuição: um nome à esquerda, o sinal de igual, e um valor à direita.

**[00:04:05] Bloco 10** · _código: célula 2, linhas 1–1_  
`ORIGEM` recebe o texto "Entrada Principal". Um texto entre aspas é uma string, o tipo `str`. O sinal de igual, em Python, não é comparação: significa “guarde este valor neste nome”.

**[00:04:18] Bloco 11** · _código: célula 2, linhas 2–2_  
`DESTINO` recebe "Mesa 4". Esses dois nomes são a consulta padrão usada nas demonstrações da Fase 1.

**[00:04:26] Bloco 12** · _código: célula 2, linhas 3–3_  
`VELOCIDADE_BASE_KMH` recebe 15.0. O ponto faz desse número um `float`, um número com casas decimais. Tudo depois do símbolo de cerquilha é comentário: o Python ignora.

**[00:04:39] Bloco 13** · _código: célula 2, linhas 1–3_  
Os nomes estão em maiúsculas por convenção: em Python, isso avisa ao leitor que o valor é uma constante, que não deve mudar durante o programa. A linguagem não proíbe a mudança; é um combinado.

**[00:04:51] Bloco 14** · _tabela: Bibliotecas importadas no projeto_  
Agora as bibliotecas. Uma biblioteca é um conjunto de código pronto que importamos para não reescrever tudo do zero.

**[00:04:59] Bloco 15** · _tabela: Bibliotecas importadas no projeto_  
Estas sete são nativas: já vêm com o Python. `perf_counter` mede tempo com precisão, `median` calcula mediana, `json` lê e grava texto estruturado e `random` sorteia números.

**[00:05:11] Bloco 16** · _tabela: Bibliotecas importadas no projeto_  
`Path` cuida de pastas e arquivos. `re` trabalha com expressões regulares, `unicodedata` separa letras de acentos, e `get_close_matches` encontra palavras parecidas.

**[00:05:23] Bloco 17** · _tabela: Bibliotecas externas_  
As externas precisam ser instaladas. Matplotlib desenha os gráficos. NumPy faz contas com vetores, e pandas organiza os dados em tabelas.

**[00:05:34] Bloco 18** · _tabela: Bibliotecas externas_  
O scikit-learn fornece os modelos de aprendizado e as métricas. PyTorch e transformers carregam e executam o modelo de linguagem Qwen.

**[00:05:44] Bloco 19** · _código: célula 19, linhas 2–14_  
Repare que existem três formas de importar. Aqui, na seção da Fase 2, aparecem todas.

**[00:05:51] Bloco 20** · _código: célula 19, linhas 2–2_  
`import json` traz o módulo inteiro; depois usamos `json.dumps`, com o nome do módulo, um ponto e a função.

**[00:05:59] Bloco 21** · _código: célula 19, linhas 5–6_  
`import numpy as np` faz o mesmo, mas dá um apelido curto. Por isso o código escreve `np.maximum` em vez de `numpy.maximum`.

**[00:06:08] Bloco 22** · _código: célula 19, linhas 11–11_  
E `from sklearn.linear_model import LinearRegression` traz só um nome de dentro do módulo. Depois ele é usado direto, sem prefixo.

**[00:06:17] Bloco 23** · _código: célula 18, linhas 1–1_  
Um último detalhe. Células como `%pip -q install numpy pandas scikit-learn` não são Python: o símbolo de porcentagem indica um comando mágico do Jupyter, que instala pacotes na sessão.

**[00:06:29] Bloco 24** · _código: célula 15, linhas 1–1 | código: célula 21, linhas 1–1_  
Há mais duas células assim: uma instala o Matplotlib, antes dos gráficos, e outra instala o transformers, antes de carregar o Qwen.

**[00:06:38] Bloco 25** · _código: célula 18, linhas 1–1_  
A opção `-q` deixa a instalação silenciosa. No Colab, a maioria desses pacotes já vem instalada, e o comando só confirma. Agora que sabemos onde o código mora, vamos à linguagem.

## Capítulo 3 — Python essencial, com o código do projeto  (início 00:06:51, duração 00:08:57)

**[00:06:51] Bloco 1** · _titulo: Python essencial_  
Capítulo três. Aqui vamos aprender os elementos de Python que aparecem no projeto, sempre com exemplos tirados do próprio código.

**[00:06:59] Bloco 2** · _cartoes: Os tipos que aparecem no projeto_  
Comece pelos tipos de dados. Todo valor em Python tem um tipo, e o tipo decide o que você pode fazer com ele.

**[00:07:07] Bloco 3** · _cartoes: Os tipos que aparecem no projeto_  
Texto é `str`. Número inteiro é `int`, como os 60 metros de uma ligação. Número com casas decimais é `float`, como os 15.0 quilômetros por hora.

**[00:07:18] Bloco 4** · _cartoes: Os tipos que aparecem no projeto_  
`bool` só tem dois valores, `True` e `False`, e é o resultado de comparações. `None` significa “nenhum valor”: `buscar` devolve `None` quando não existe caminho.

**[00:07:28] Bloco 5** · _cartoes: Os tipos que aparecem no projeto_  
Depois vêm as estruturas que guardam vários valores. Uma lista, entre colchetes, é uma sequência ordenada que pode crescer: `LOCAIS` é uma lista de nomes.

**[00:07:39] Bloco 6** · _cartoes: Os tipos que aparecem no projeto_  
Uma tupla, entre parênteses, também é uma sequência, mas não pode ser alterada depois de criada. Cada ligação do mapa é uma tupla: origem, destino e metros.

**[00:07:51] Bloco 7** · _cartoes: Os tipos que aparecem no projeto_  
Um dicionário, entre chaves, guarda pares de chave e valor. Em `VIZINHOS`, a chave é o nome do local e o valor é a lista dos vizinhos.

**[00:08:00] Bloco 8** · _cartoes: Os tipos que aparecem no projeto_  
E um conjunto, o `set`, guarda valores sem repetição e sem ordem. O projeto usa `set` em `preparar_pedido` para descobrir parâmetros extras.

**[00:08:10] Bloco 9** · _topicos: Por que cada estrutura_  
Por que escolher cada um? A lista serve quando a ordem importa, como no caminho. A tupla protege dados que não devem mudar. O dicionário permite achar um valor pela chave muito rápido.

**[00:08:23] Bloco 10** · _código: célula 7, linhas 19–19_  
Agora os três tipos de parênteses, que confundem muita gente. Olhe esta linha da busca.

**[00:08:30] Bloco 11** · _código: célula 7, linhas 19–19_  
Os colchetes de fora criam uma lista. Dentro dela há uma tupla, entre parênteses, com quatro valores. E o último valor é outra lista, com a origem dentro.

**[00:08:40] Bloco 12** · _código: célula 7, linhas 23–32_  
Parênteses também servem para chamar funções, como em `min(fronteira)`. Colchetes também servem para pegar um item: `grafo[local]` pega o valor guardado na chave `local`.

**[00:08:51] Bloco 13** · _código: célula 5, linhas 96–101_  
Índices começam em zero. Em `PONTOS_IJ[indice - 1]`, o código pega o item anterior da lista. E em `caminho[1:]`, os dois-pontos fazem uma fatia: todos os itens a partir do segundo.

**[00:09:06] Bloco 14** · _código: célula 28, linhas 19–20_  
Fatias com número negativo contam do fim. Na conversa interativa, `[-4:]` guarda só as quatro últimas mensagens do histórico.

**[00:09:17] Bloco 15** · _código: célula 7, linhas 63–63_  
Operadores aritméticos fazem contas. Nesta linha, a distância em metros vezes 3,6, dividida pela velocidade em quilômetros por hora, dá o tempo em segundos.

**[00:09:28] Bloco 16** · _formula: A conversão de `calcular_tempo`_  
Por que 3,6? Porque um metro por segundo equivale a 3,6 quilômetros por hora. Para 89,5 metros a 15 quilômetros por hora, a conta dá 21,48 segundos.

**[00:09:43] Bloco 17** · _código: célula 7, linhas 26–33_  
Operadores de comparação devolvem `True` ou `False`: igual é dois sinais de igual, diferente é exclamação e igual, e existem menor e maior. `in` testa se um valor está dentro de uma coleção.

**[00:09:55] Bloco 18** · _código: célula 7, linhas 57–58_  
Operadores lógicos combinam condições: `and` exige as duas, `or` aceita uma delas, e `not` inverte. Aqui o teste rejeita velocidade que não é número, ou que é booleana.

**[00:10:06] Bloco 19** · _código: célula 7, linhas 22–31_  
Repare nos dois-pontos no fim de `if`, `for`, `while` e `def`. Eles abrem um bloco. E o bloco é definido pela indentação: as linhas recuadas com quatro espaços pertencem a ele.

**[00:10:19] Bloco 20** · _código: célula 7, linhas 26–29_  
Em muitas linguagens, o bloco é marcado com chaves. Em Python, a indentação faz parte da sintaxe: se você recuar errado, o programa muda de significado ou dá erro.

**[00:10:30] Bloco 21** · _código: célula 7, linhas 13–13_  
Agora as funções. A palavra `def` cria uma função; em seguida vêm o nome, os parâmetros entre parênteses e os dois-pontos.

**[00:10:39] Bloco 22** · _código: célula 7, linhas 13–13_  
Parâmetros são os nomes que a função recebe. Argumentos são os valores que você passa na chamada. Em `buscar("Mesa 1", "Mesa 4", VIZINHOS, True)`, "Mesa 1" é o argumento do parâmetro `origem`.

**[00:10:53] Bloco 23** · _código: célula 7, linhas 13–15_  
`referencia=None` é um parâmetro com valor padrão. Se a chamada não informar a referência, ela vale `None`, e as linhas 14 e 15 trocam por `DISTANCIA_ENTRADA`.

**[00:11:04] Bloco 24** · _código: célula 7, linhas 27–27_  
`return` encerra a função e devolve um valor para quem chamou. Aqui a função devolve três valores separados por vírgula, e o Python os junta numa tupla.

**[00:11:14] Bloco 25** · _código: célula 7, linhas 42–42_  
Do outro lado, quem chama desempacota a tupla em três nomes de uma vez, como faz `a_estrela` na linha 42.

**[00:11:21] Bloco 26** · _código: célula 22, linhas 20–24_  
Escopo é onde um nome existe. Variáveis criadas dentro de uma função são locais: somem quando ela termina. Nomes criados fora, no nível da célula, são globais e todas as funções podem ler.

**[00:11:35] Bloco 27** · _código: célula 22, linhas 24–37_  
Para alterar uma variável global dentro de uma função, é preciso declarar `global`, como faz `conversar` com `ULTIMA_GERACAO`. Sem isso, a atribuição criaria uma variável local nova.

**[00:11:46] Bloco 28** · _código: célula 7, linhas 23–24_  
Agora a diferença entre função e método. Uma função existe sozinha: `min(fronteira)`. Um método pertence a um objeto e é chamado com um ponto: `fronteira.remove(melhor)`.

**[00:11:58] Bloco 29** · _código: célula 7, linhas 30–30_  
O ponto significa “acesse algo que pertence a este objeto”. Em Python, tudo é objeto: uma lista sabe se remover itens, uma string sabe se transformar. O ponto dá acesso a esses atributos e métodos.

**[00:12:12] Bloco 30** · _código: célula 39, linhas 3–3_  
Vamos ver isso em detalhe com uma expressão real do projeto: `pergunta.strip().lower()`, na última célula do notebook.

**[00:12:20] Bloco 31** · _código: célula 39, linhas 2–2_  
`pergunta` é uma variável. Ela recebe o que a função `input` devolve, e `input` sempre devolve uma string, o texto que a pessoa digitou.

**[00:12:28] Bloco 32** · _transformacao: `pergunta.strip().lower()`_  
O primeiro ponto acessa um método da string. `strip` remove espaços e quebras de linha do começo e do fim. Os parênteses depois do nome executam o método; sem eles, você só teria uma referência ao método.

**[00:12:42] Bloco 33** · _transformacao: `pergunta.strip().lower()`_  
Quando `strip()` roda, ele não altera a string original: strings são imutáveis em Python. Ele cria e devolve uma string nova, sem os espaços.

**[00:12:52] Bloco 34** · _transformacao: `pergunta.strip().lower()`_  
O segundo ponto é aplicado sobre esse valor devolvido. Isso se chama encadeamento de métodos. `lower` converte as letras para minúsculas e devolve outra string nova.

**[00:13:03] Bloco 35** · _transformacao: `pergunta.strip().lower()`_  
A ordem é da esquerda para a direita: primeiro `strip`, depois `lower`. No fim, `pergunta` continua igual; só o valor da expressão é usado na comparação.

**[00:13:13] Bloco 36** · _código: célula 39, linhas 2–8_  
Por isso a expressão funciona dentro do `while`: a condição é “enquanto o texto limpo for diferente de sair”. Assim, “ SAIR ”, com espaços e maiúsculas, também encerra a conversa.

**[00:13:25] Bloco 37** · _código: célula 39, linhas 3–3_  
E se tirássemos um dos métodos? Sem `strip`, “sair ” com espaço não encerraria. Sem `lower`, “Sair” com maiúscula não encerraria. Cada método resolve um problema real de digitação.

**[00:13:38] Bloco 38** · _código: célula 5, linhas 105–110_  
Agora os laços. O `for` percorre uma coleção item por item. Aqui ele percorre cada tupla de `LIGACOES` e já separa os três valores em `origem`, `destino` e `metros`.

**[00:13:50] Bloco 39** · _código: célula 7, linhas 22–22_  
O `while` repete enquanto a condição for verdadeira. A busca roda enquanto houver itens na fronteira, porque não se sabe antes quantas voltas serão necessárias.

**[00:14:00] Bloco 40** · _código: célula 28, linhas 4–15_  
`continue` pula para a próxima volta do laço, ignorando o resto do bloco. `break` sai do laço de vez. Na conversa interativa, digitar sair executa `break`.

**[00:14:11] Bloco 41** · _código: célula 19, linhas 24–30_  
Três funções ajudam nos laços. `range(12)` gera os números de 0 a 11. `enumerate` devolve o índice junto com o item. E `zip` percorre duas listas lado a lado.

**[00:14:23] Bloco 42** · _código: célula 7, linhas 18–18_  
Há também uma forma curta de `if`, a expressão condicional: valor se condição, senão outro valor. Aqui, a estimativa vale a fórmula da heurística se `usar_heuristica` for verdadeiro, ou zero.

**[00:14:36] Bloco 43** · _código: célula 7, linhas 53–53_  
As f-strings montam textos com valores dentro. A letra f antes das aspas permite colocar expressões entre chaves, e `:.3f` formata o número com três casas decimais.

**[00:14:48] Bloco 44** · _código: célula 13, linhas 28–28_  
Uma lambda é uma função pequena e sem nome, escrita numa linha. Aqui ela diz ao `max` qual valor comparar: a distância de cada local até a entrada.

**[00:14:58] Bloco 45** · _código: célula 24, linhas 34–34_  
Compreensões de lista criam uma lista nova a partir de outra numa linha só. Esta pega todos os locais cujo nome começa com WC: a lista de banheiros.

**[00:15:08] Bloco 46** · _código: célula 7, linhas 56–63_  
Por fim, as exceções, que são erros sinalizados. `raise ValueError` dispara um erro de propósito quando a velocidade é inválida.

**[00:15:17] Bloco 47** · _código: célula 9, linhas 11–14_  
E `try` com `except` captura um erro para o programa não parar. Em `calcular_rota`, se a velocidade fosse inválida, o erro vira uma mensagem de texto em vez de derrubar o notebook.

**[00:15:28] Bloco 48** · _código: célula 19, linhas 65–69_  
O `assert` confere uma condição e para o programa se ela for falsa. O projeto usa `assert` para garantir que os dados gerados não têm valores faltando.

**[00:15:38] Bloco 49** · _titulo: Próximo: o campus vira um grafo_  
Pronto: com esses elementos, você consegue ler qualquer linha do projeto. No próximo capítulo, vamos ver como o campus do IESB vira um grafo.

## Capítulo 4 — O campus vira um grafo  (início 00:15:48, duração 00:06:09)

**[00:15:48] Bloco 1** · _titulo: O campus vira um grafo_  
Capítulo quatro. Como o térreo do IESB, com corredores, salas e mesas, se transforma numa estrutura de dados que um algoritmo consegue percorrer?

**[00:15:58] Bloco 2** · _imagem: Planta de referência do térreo (referencias/planta_terreo_iesb.png)_  
Tudo começa na planta do térreo. Ela é a referência do grupo para decidir quais locais existem e quais estão ligados.

**[00:16:06] Bloco 3** · _grafo do campus_  
Um grafo é um conjunto de nós ligados por arestas. No projeto, cada nó é um local, como uma sala, uma mesa ou um ponto de corredor. Cada aresta é uma passagem entre dois locais.

**[00:16:20] Bloco 4** · _grafo do campus_  
O grafo final tem 90 nós e 90 ligações. Como existe exatamente um ciclo, no pátio, o número de ligações é igual ao de nós: uma árvore teria 89.

**[00:16:31] Bloco 5** · _grafo do campus_  
Cada ligação tem um peso: a distância estimada em metros. O peso é o custo de atravessar aquela aresta. Na Fase 1, o melhor caminho é o de menor soma de pesos.

**[00:16:43] Bloco 6** · _grafo do campus_  
Atenção a um ponto que costuma aparecer na arguição: o projeto não guarda coordenadas. As posições que você vê na tela foram escolhidas só para desenhar. O algoritmo só conhece nomes e metros.

**[00:16:56] Bloco 7** · _grafo do campus_  
As ligações são bidirecionais: se dá para ir de A até B, dá para voltar de B até A, com o mesmo custo. Isso é um grafo não direcionado.

**[00:17:06] Bloco 8** · _código: célula 5, linhas 1–18_  
Agora o código. A seção 2 começa com a lista `LOCAIS`, entre colchetes, com o nome de cada local como string.

**[00:17:14] Bloco 9** · _código: célula 5, linhas 21–41_  
Depois vem `LIGACOES`, uma lista de tuplas. Cada tupla tem três valores: origem, destino e a distância estimada em metros.

**[00:17:23] Bloco 10** · _código: célula 5, linhas 23–27_  
A primeira diz que da Entrada Principal ao Eixo Norte são 60 metros. O eixo principal soma 210 metros, dividido em trechos de 60, 48, 39, 39 e 24.

**[00:17:37] Bloco 11** · _código: célula 5, linhas 28–28_  
Repare no valor 27.5 na linha 28: o tipo pode ser `int` ou `float` na mesma lista, porque Python só se importa com o tipo na hora da conta.

**[00:17:46] Bloco 12** · _código: célula 5, linhas 43–45_  
Em seguida, o pátio. O método `extend` acrescenta vários itens de uma vez ao fim da lista: os três pontos de circulação A, B e D.

**[00:17:56] Bloco 13** · _código: célula 5, linhas 46–56_  
E `LIGACOES.extend` acrescenta as ligações do pátio. A, B, Pátio Direito e D formam um quadrado: este é o único ciclo do grafo. As mesas ficam a 2 metros dos pontos.

**[00:18:09] Bloco 14** · _código: célula 5, linhas 57–61_  
As três últimas ligações do pátio levam aos apoios: Sala dos Professores, com 15 metros, e os dois banheiros do pátio, com 40 e 35. O comentário avisa que essas posições ainda não foram revisadas.

**[00:18:23] Bloco 15** · _grafo do campus_  
No desenho, o ciclo é este quadrado. Por causa dele, existem dois caminhos entre a Mesa 1 e a Mesa 4: por B ou por D. Isso vai ser importante na Fase 2.

**[00:18:36] Bloco 16** · _código: célula 5, linhas 63–64_  
A partir daqui, o código usa laços para não escrever cada ligação à mão. Este `for` percorre uma lista de duas tuplas e acrescenta as ligações do Cinema até o WC do Cinema e o Anexo Creche.

**[00:18:49] Bloco 17** · _código: célula 5, linhas 68–82_  
Este laço maior monta os três corredores, Design, Bloco C e Bloco B, de um jeito só. Cada volta recebe o nome do corredor, a letra das salas e o sufixo dos banheiros.

**[00:19:01] Bloco 18** · _código: célula 5, linhas 73–77_  
A variável `anterior` começa no próprio corredor. O laço interno cria um ponto por par de salas, por exemplo "Corredor Design - 03/06", e o liga ao ponto anterior com 10 metros.

**[00:19:12] Bloco 19** · _código: célula 5, linhas 75–75_  
A expressão `"/".join(salas)` junta as strings da tupla com uma barra no meio: de ("03", "06") sai "03/06". `join` é um método da string separadora.

**[00:19:23] Bloco 20** · _código: célula 5, linhas 78–79_  
Para cada sala do par, uma ligação de 2 metros vai do ponto até a sala. O nome da sala é montado com soma de strings: "D" mais hífen mais "03" dá "D-03".

**[00:19:35] Bloco 21** · _código: célula 5, linhas 80–80_  
No fim de cada volta, `anterior` passa a ser o ponto atual. Assim, a próxima volta liga o novo ponto ao anterior, formando uma corrente: corredor, 03/06, 02/05, 01/04.

**[00:19:47] Bloco 22** · _grafo do campus_  
No desenho, cada corredor vira esta escada: um caminho de pontos com salas dos dois lados e os banheiros perto da entrada do corredor.

**[00:19:56] Bloco 23** · _código: célula 5, linhas 85–95_  
O corredor I e J é feito com outra ideia: cada ponto tem uma posição em metros a partir do acesso lateral, de menos 35 a mais 35.

**[00:20:05] Bloco 24** · _código: célula 5, linhas 96–101_  
O laço usa `enumerate` para saber o índice. Se o ponto ainda não está em `LOCAIS`, ele é incluído. A partir do segundo, liga ao ponto anterior com a diferença de posições.

**[00:20:17] Bloco 25** · _código: célula 5, linhas 100–100_  
Por exemplo: de menos 35 para menos 25, a ligação tem 10 metros. O sublinhado em `anterior, posicao_anterior, _` é um nome descartável: o terceiro valor não é usado.

**[00:20:29] Bloco 26** · _código: célula 5, linhas 102–103_  
No fim de cada volta, um `for` interno liga o ponto às suas salas ou banheiros, com 2 metros cada. O ponto central, "Corredor I/J", tem a lista vazia e não liga a nenhuma sala.

**[00:20:41] Bloco 27** · _código: célula 5, linhas 105–107_  
Agora a peça mais importante: o dicionário `VIZINHOS`. Primeiro, cada local recebe uma lista vazia.

**[00:20:49] Bloco 28** · _código: célula 5, linhas 108–110_  
Depois, para cada ligação, o vizinho é acrescentado nos dois sentidos: o destino na lista da origem, e a origem na lista do destino. É isso que torna o grafo bidirecional.

**[00:21:00] Bloco 29** · _grafo do campus_  
Essa estrutura se chama lista de adjacência. Para saber para onde o carrinho pode ir a partir de um local, basta ler `VIZINHOS[local]`.

**[00:21:09] Bloco 30** · _código: célula 9, linhas 25–37 | terminal: listar_vizinhos("Pátio/Direito")_  
A função `listar_vizinhos` faz exatamente isso. Para o Pátio Direito, o resultado real é: Eixo Norte, Pátio B, Pátio D, Mesa 4, Sala dos Professores e os dois banheiros do pátio.

**[00:21:22] Bloco 31** · _topicos: Por que lista de adjacência_  
Por que um dicionário de listas, e não uma matriz de 90 por 90? Porque cada local tem poucos vizinhos. A matriz guardaria 8100 posições, quase todas vazias.

**[00:21:34] Bloco 32** · _código: célula 5, linhas 112–112 | terminal: Saída da seção 2_  
A célula termina imprimindo o tamanho do grafo. A saída real é: 90 nós e 90 ligações com distância em metros.

**[00:21:43] Bloco 33** · _topicos: O problema em espaço de estados_  
Resumo em termos de Inteligência Artificial: o estado é o local atual do carrinho; o estado inicial é a origem; as ações são mover para um vizinho; o teste de objetivo é chegar ao destino; e o custo de cada ação é o peso da ligação.

## Capítulo 5 — A busca de custo uniforme  (início 00:21:57, duração 00:06:03)

**[00:21:57] Bloco 1** · _titulo: A busca e o custo uniforme_  
Capítulo cinco. Já temos o grafo. Agora, como um programa encontra o melhor caminho dentro dele? Esta é a pergunta da busca em Inteligência Artificial.

**[00:22:08] Bloco 2** · _topicos: Busca em IA_  
Buscar é explorar estados a partir da origem até achar o objetivo. Uma busca não informada só conhece o custo já percorrido. Uma busca informada usa também uma estimativa do que falta.

**[00:22:21] Bloco 3** · _formula: Custo uniforme_  
A busca de custo uniforme sempre expande o nó de menor custo acumulado desde a origem. Esse custo se chama g. Com custos positivos, o primeiro caminho que chega ao destino é o mais barato.

**[00:22:34] Bloco 4** · _código: célula 7, linhas 13–13_  
Agora a função `buscar`, linha por linha. Ela recebe a origem, o destino, o grafo, um booleano dizendo se usa a heurística, e a tabela de referência da heurística.

**[00:22:45] Bloco 5** · _código: célula 7, linhas 14–17_  
Se a referência não for passada, usa a tabela `DISTANCIA_ENTRADA`. E se a origem ou o destino não existirem no grafo, a função devolve `None`, `None` e zero, sem procurar.

**[00:22:56] Bloco 6** · _código: célula 7, linhas 18–18_  
A linha 18 calcula a estimativa da origem. No custo uniforme, `usar_heuristica` é falso, então a estimativa é zero.

**[00:23:05] Bloco 7** · _código: célula 7, linhas 19–19_  
A fronteira é a lista dos caminhos que ainda podem ser explorados. Cada item é uma tupla com quatro valores: f, g, o local e o caminho até ele.

**[00:23:15] Bloco 8** · _código: célula 7, linhas 20–21_  
`visitados` guarda os locais já expandidos, e `expandidos` conta quantos foram. Essa contagem é a métrica do experimento.

**[00:23:24] Bloco 9** · _código: célula 7, linhas 22–22_  
O laço `while` roda enquanto a fronteira não estiver vazia. A cada volta, ele escolhe um item, testa e, se for o caso, expande.

**[00:23:33] Bloco 10** · _código: célula 7, linhas 38–38_  
Se a fronteira esvaziar sem achar o destino, não existe caminho entre os dois locais, e a linha 38, já fora do laço, devolve `None`, `None` e a contagem de expandidos.

**[00:23:45] Bloco 11** · _código: célula 7, linhas 23–23_  
`min(fronteira)` escolhe a menor tupla. Python compara tuplas posição por posição: primeiro o f, depois o g, depois o nome do local. Por isso a primeira posição da tupla é a prioridade.

**[00:23:57] Bloco 12** · _código: célula 7, linhas 23–24_  
Esta é a fila de prioridade do projeto: uma lista comum com `min`. Em projetos grandes se usa `heapq`, que é mais rápido; aqui, com 90 nós, a lista simples é suficiente e mais fácil de explicar.

**[00:24:11] Bloco 13** · _código: célula 7, linhas 25–27_  
A linha 25 desempacota a tupla escolhida em quatro nomes. Se o local é o destino, a busca termina e devolve o caminho, o custo g e os expandidos.

**[00:24:22] Bloco 14** · _código: célula 7, linhas 26–26_  
Detalhe importante: o teste de objetivo acontece quando o nó sai da fronteira, e não quando entra. É isso que garante o caminho mais barato.

**[00:24:31] Bloco 15** · _código: célula 7, linhas 28–29_  
Se o local já foi visitado, `continue` pula para a próxima volta. Isso descarta cópias antigas e piores do mesmo local que ficaram na fronteira.

**[00:24:40] Bloco 16** · _código: célula 7, linhas 30–34_  
Senão, o local entra em `visitados` e o contador aumenta. Depois, o `for` percorre os vizinhos. Para cada vizinho ainda não visitado, calcula o novo g: o g atual mais o custo da ligação.

**[00:24:54] Bloco 17** · _código: célula 7, linhas 35–37_  
E acrescenta na fronteira uma tupla nova, com o caminho estendido. Repare que `caminho + [vizinho]` cria uma lista nova: o caminho de cada item da fronteira é independente.

**[00:25:04] Bloco 18** · _grafo do campus | tabela: Fronteira (custo uniforme)_  
Vamos ver tudo isso funcionando com dados reais: custo uniforme da Mesa 1 até a Mesa 4. Estas são exatamente as voltas que a função executa.

**[00:25:14] Bloco 19** · _grafo do campus | tabela: Fronteira (custo uniforme)_  
Volta 1. A fronteira tem só a origem, Mesa 1, com custo zero. Ela é escolhida, não é o destino e ainda não foi visitada. Então é expandida: seu único vizinho, Pátio A, entra com g igual a 2.

**[00:25:29] Bloco 20** · _grafo do campus | tabela: Fronteira (custo uniforme)_  
Volta 2. O único item é Pátio A, com g 2. Ao expandir, entram Pátio B, com 2 mais 20, igual a 22, e Pátio D, com 2 mais 18, igual a 20. Mesa 1 já foi visitada e não volta.

**[00:25:45] Bloco 21** · _grafo do campus | tabela: Fronteira (custo uniforme)_  
Volta 3. O menor custo é Pátio D, com 20. Ele entra em visitados, e seus vizinhos entram: Pátio Direito com 44 e Mesa 3 com 22.

**[00:25:57] Bloco 22** · _grafo do campus | tabela: Fronteira (custo uniforme)_  
Volta 4. Agora há um empate em 22: Mesa 3 e Pátio B. O `min` compara tuplas posição por posição: f igual, g igual, então desempata pelo nome. “Mesa 3” vem antes de “Pátio B” na ordem alfabética.

**[00:26:12] Bloco 23** · _grafo do campus | tabela: Fronteira (custo uniforme)_  
Mesa 3 é expandida, mas não tem vizinhos novos. Volta 5: Pátio B, com 22, é expandido. Entram Pátio Direito com 40, Mesa 2 e Easy Smart com 24, e Café Mania com 26.

**[00:26:28] Bloco 24** · _grafo do campus | tabela: Fronteira (custo uniforme)_  
Repare que Pátio Direito aparece duas vezes na fronteira: com 44, vindo por D, e com 40, vindo por B. O código não apaga a cópia pior; ela fica lá e será ignorada se for escolhida depois.

**[00:26:42] Bloco 25** · _grafo do campus | tabela: Fronteira (custo uniforme)_  
Voltas 6, 7 e 8: Easy Smart, Mesa 2 e Café Mania, todos perto de 24 e 26, são expandidos e não acrescentam nada. A busca gasta tempo com eles porque não sabe onde fica o destino.

**[00:26:57] Bloco 26** · _grafo do campus | tabela: Fronteira (custo uniforme)_  
Volta 9. O menor agora é Pátio Direito com 40. Ao expandi-lo, Mesa 4 entra com 40 mais 2, igual a 42, junto com o Eixo Norte, a Sala dos Professores e os banheiros.

**[00:27:10] Bloco 27** · _grafo do campus (caminho Mesa 1 → Pátio - A → Pátio - B → Pátio/Direito → Mesa 4) | tabela: Fronteira (custo uniforme)_  
Volta 10. O menor custo é Mesa 4, com 42. Agora sim, ao ser retirada da fronteira, ela é o destino. A função devolve o caminho, o custo 42 e 9 nós expandidos.

**[00:27:25] Bloco 28** · _grafo do campus (caminho Mesa 1 → Pátio - A → Pátio - B → Pátio/Direito → Mesa 4; carrinho animado)_  
O carrinho segue o caminho encontrado: Mesa 1, Pátio A, Pátio B, Pátio Direito e Mesa 4, com 42 metros no total.

**[00:27:34] Bloco 29** · _topicos: Custo uniforme: balanço_  
Vantagens do custo uniforme: é completo, porque acha um caminho se ele existir, e é ótimo com custos positivos. A limitação: expande em todas as direções, inclusive para longe do destino.

**[00:27:47] Bloco 30** · _titulo: Próximo: a heurística_  
Neste exemplo, ele expandiu 9 nós, incluindo Mesa 3, Easy Smart, Mesa 2 e Café Mania, que não ajudam a chegar à Mesa 4. No próximo capítulo, vamos dar uma direção à busca: a heurística.

## Capítulo 6 — Heurística: uma estimativa que aponta o caminho  (início 00:28:01, duração 00:04:09)

**[00:28:01] Bloco 1** · _titulo: Heurística_  
Capítulo seis, só sobre heurística. É uma das partes mais cobradas na arguição, então vamos com calma.

**[00:28:08] Bloco 2** · _formula: O que é uma heurística_  
Uma heurística é uma estimativa de quanto falta para chegar ao objetivo, a partir de um nó. Chamamos essa estimativa de h de n.

**[00:28:17] Bloco 3** · _topicos: Para que serve_  
Ela existe para dar direção. O custo uniforme olha só para trás, para o custo já pago. A heurística olha para a frente e diz quais nós parecem mais perto do destino.

**[00:28:28] Bloco 4** · _topicos: Custo real × custo estimado_  
Atenção à diferença: o custo real é a menor soma de metros até o destino, que só conhecemos depois da busca. O custo estimado é um palpite calculado antes, de forma barata.

**[00:28:40] Bloco 5** · _topicos: Por que não a distância euclidiana_  
O exemplo clássico de heurística é a distância em linha reta, a euclidiana. Mas ela exige coordenadas de cada local, e este projeto não tem coordenadas: só nomes e metros das ligações.

**[00:28:53] Bloco 6** · _código: célula 7, linhas 1–4_  
A seção 3 começa importando `perf_counter`, do módulo `time`, e criando `DISTANCIA_ENTRADA` como um dicionário vazio, que será preenchido logo depois.

**[00:29:02] Bloco 7** · _código: célula 7, linhas 46–53_  
A solução do grupo foi usar um ponto de referência: a Entrada Principal. Antes de qualquer consulta, o código calcula a menor distância da entrada até cada um dos 90 locais.

**[00:29:14] Bloco 8** · _código: célula 7, linhas 49–51_  
O laço percorre `LOCAIS` e, para cada um, chama `buscar` da entrada até ele, com `usar_heuristica` falso, ou seja, custo uniforme. O custo devolvido vai para o dicionário `DISTANCIA_ENTRADA`.

**[00:29:27] Bloco 9** · _código: célula 7, linhas 48–53_  
`perf_counter` marca o tempo antes e depois, e a diferença vezes mil dá milissegundos. Na execução real, essa preparação levou cerca de 3 milissegundos, uma vez só.

**[00:29:38] Bloco 10** · _grafo do campus | tabela: DISTANCIA_ENTRADA (metros)_  
Estes são os valores reais da tabela para alguns locais. A Mesa 4 fica a 89,5 metros da entrada; a Mesa 1, a 127,5.

**[00:29:50] Bloco 11** · _formula: A heurística do projeto_  
Agora a fórmula. A estimativa de um local até o destino é o valor absoluto da diferença entre as distâncias dos dois até a entrada.

**[00:29:59] Bloco 12** · _código: célula 7, linhas 35–35_  
No código, ela aparece dentro de `buscar`, na linha 35. `abs` é a função de valor absoluto. E `referencia.get(vizinho, 0)` busca a distância no dicionário, com zero se o local não estiver lá.

**[00:30:12] Bloco 13** · _código: célula 7, linhas 7–10_  
Existe também uma função `h` na linha 7, com a mesma fórmula. Mas ela não é chamada: `buscar` calcula a estimativa direto na linha, para poder trocar a tabela de referência na Fase 2.

**[00:30:25] Bloco 14** · _formula: _  
Vamos calcular. Da Mesa 1 até a Mesa 4: 127,5 menos 89,5 dá 38. O custo real, que a busca achou, é 42. A estimativa ficou abaixo do real, como deve ser.

**[00:30:40] Bloco 15** · _formula: Desigualdade triangular_  
Por que ela nunca exagera? Pela desigualdade triangular: o caminho mais curto da entrada até o destino não pode ser maior que ir da entrada até n e depois de n até o destino.

**[00:30:51] Bloco 16** · _formula: Consequência_  
Passando d de E até n para o outro lado: a diferença fica menor ou igual à distância real de n até o destino. O mesmo raciocínio vale trocando os papéis, e por isso vale para o valor absoluto.

**[00:31:04] Bloco 17** · _formula: Consistência_  
Ela também é consistente: para qualquer ligação de u até v com custo c, h de u é menor ou igual a c mais h de v. Em palavras: andar uma aresta nunca faz a estimativa cair mais do que o custo da aresta.

**[00:31:18] Bloco 18** · _topicos: Quando a garantia vale_  
Essas propriedades valem porque a tabela usa os mesmos metros do grafo e é calculada com busca exata. Se alguém mudar uma distância e não reexecutar a célula, a tabela fica desatualizada e a garantia some.

**[00:31:32] Bloco 19** · _código: célula 19, linhas 150–153_  
E na Fase 2, quando o custo vira segundos? A tabela em metros não serve mais. Por isso `rota_tempo_previsto` recalcula a referência em segundos, no grafo de tempos, antes de cada busca.

**[00:31:46] Bloco 20** · _topicos: Heurística inadequada_  
E se a heurística fosse ruim? Se ela superestimar o que falta, o A* pode descartar o melhor caminho e devolver um pior. Se for zero, não atrapalha, mas também não ajuda: vira custo uniforme.

**[00:31:59] Bloco 21** · _titulo: Próximo: o A*_  
Essa fraqueza aparece quando a origem é a própria entrada: aí todos os nós no caminho têm a mesma prioridade. Vamos ver o efeito disso no próximo capítulo, sobre o A estrela.

## Capítulo 7 — O algoritmo A*  (início 00:32:11, duração 00:05:33)

**[00:32:11] Bloco 1** · _titulo: O algoritmo A*_  
Capítulo sete: o A estrela, o algoritmo central da Fase 1. Ele junta as duas ideias que já vimos: o custo já percorrido e a estimativa do que falta.

**[00:32:21] Bloco 2** · _formula: A fórmula do A*_  
A prioridade de cada nó na fronteira é f de n, a soma de g de n e h de n.

**[00:32:27] Bloco 3** · _formula: A fórmula do A*_  
g de n é o custo real já pago, da origem até n. É a soma dos metros das ligações percorridas.

**[00:32:35] Bloco 4** · _formula: A fórmula do A*_  
h de n é a estimativa do que ainda falta, de n até o destino, dada pela heurística do capítulo anterior.

**[00:32:42] Bloco 5** · _formula: A fórmula do A*_  
E f de n estima o custo total de um caminho que passa por n. Somar faz sentido porque as duas partes estão na mesma unidade, metros, e juntas cobrem o trajeto inteiro: o que já foi e o que falta.

**[00:32:56] Bloco 6** · _código: célula 7, linhas 34–37_  
No código, o A estrela é a mesma função `buscar`, com `usar_heuristica` verdadeiro. A linha 35 calcula h do vizinho, e a linha 36 guarda na fronteira o novo g mais a estimativa, que é o f.

**[00:33:10] Bloco 7** · _código: célula 7, linhas 23–23_  
Como f é a primeira posição da tupla, o `min` da linha 23 escolhe automaticamente o menor f. Em empate de f, escolhe o menor g; em empate de g, a ordem alfabética do nome.

**[00:33:22] Bloco 8** · _código: célula 7, linhas 41–43_  
A função `a_estrela` é só um atalho: chama `buscar` com o grafo de metros e a heurística ligada, e devolve o caminho e o custo.

**[00:33:30] Bloco 9** · _grafo do campus | tabela: Fronteira do A* (ordenada por f)_  
Agora, a mesma consulta do capítulo cinco, Mesa 1 até Mesa 4, com o A estrela. No início da volta 1, a fronteira tem só a origem: g zero, h 38, pois 127,5 menos 89,5 dá 38. Então f é 38.

**[00:33:48] Bloco 10** · _grafo do campus | tabela: Fronteira do A* (ordenada por f)_  
Início da volta 2. Ao expandir a Mesa 1, entrou Pátio A, com g 2 e h 36, pois 125,5 menos 89,5 dá 36. f é 38, e ele é o único da fronteira.

**[00:34:01] Bloco 11** · _grafo do campus | tabela: Fronteira do A* (ordenada por f)_  
Início da volta 3. Ao expandir Pátio A, entraram Pátio B, com g 22 e h 16, f 38, e Pátio D, com g 20 e h 22, f 42. Repare: D tem g menor, mas B parece mais perto do destino.

**[00:34:19] Bloco 12** · _grafo do campus | tabela: Fronteira do A* (ordenada por f)_  
Por isso o A estrela escolhe Pátio B, com f 38. O custo uniforme tinha escolhido Pátio D, só porque o g era menor. A heurística mudou a ordem.

**[00:34:30] Bloco 13** · _grafo do campus | tabela: Fronteira do A* (ordenada por f)_  
Início da volta 4. Pátio B foi expandido e entraram Pátio Direito, Mesa 2 e Easy Smart, todos com f 42, e Café Mania, com f 46.

**[00:34:42] Bloco 14** · _grafo do campus | tabela: Fronteira do A* (ordenada por f)_  
Agora há vários empates em 42. Pela regra da tupla, ganha o menor g: Pátio D, com g 20. Ao ser expandido, ele acrescenta Mesa 3 e uma segunda cópia de Pátio Direito, as duas com f 46.

**[00:34:57] Bloco 15** · _grafo do campus | tabela: Fronteira do A* (ordenada por f)_  
Voltas 5 e 6: Easy Smart e Mesa 2, com f 42 e g 24, são expandidos sem novidade. Os empates fazem o A estrela gastar duas expansões que não ajudam.

**[00:35:10] Bloco 16** · _grafo do campus | tabela: Fronteira do A* (ordenada por f)_  
Início da volta 7. Pátio Direito, com g 40 e h 2, f 42, é escolhido e expandido. Mesa 4 entra com g 42 e h zero: f 42.

**[00:35:23] Bloco 17** · _grafo do campus (caminho Mesa 1 → Pátio - A → Pátio - B → Pátio/Direito → Mesa 4) | tabela: Fronteira do A* (ordenada por f)_  
Volta 8. Mesa 4 é retirada com f 42 e é o destino. Caminho: Mesa 1, Pátio A, Pátio B, Pátio Direito, Mesa 4. Custo 42 metros, o mesmo do custo uniforme.

**[00:35:38] Bloco 18** · _tabela: Mesma consulta, Mesa 1 → Mesa 4 (valores reais)_  
A diferença está no trabalho: o A estrela expandiu 7 nós, contra 9 do custo uniforme. Mesa 3 e Café Mania ficaram na fronteira com f 46 e nunca precisaram ser expandidos.

**[00:35:51] Bloco 19** · _grafo do campus (caminho Mesa 1 → Pátio - A → Pátio - B → Pátio/Direito → Mesa 4; carrinho animado)_  
Veja o carrinho percorrendo o caminho escolhido.

**[00:35:55] Bloco 20** · _topicos: Quando o A* é ótimo_  
Quando o A estrela garante o caminho ótimo? Quando a heurística é admissível e o objetivo é testado ao retirar o nó da fronteira, como na linha 26.

**[00:36:05] Bloco 21** · _código: célula 7, linhas 26–27_  
Por que o primeiro caminho encontrado pode não ser ótimo em outras implementações? Se o teste de objetivo fosse feito ao inserir o vizinho, um caminho caro poderia ser devolvido antes de outro mais barato aparecer.

**[00:36:19] Bloco 22** · _formula: _  
E se a heurística for zero? Então f é igual a g, e o A estrela vira exatamente o custo uniforme. É isso que o projeto faz quando `usar_heuristica` é falso.

**[00:36:30] Bloco 23** · _tabela: Três buscas, uma diferença: a prioridade_  
E a busca gulosa? Ela usa só h de n, ignorando o custo já pago. É rápida, mas não garante o melhor caminho. O A estrela equilibra as duas coisas.

**[00:36:41] Bloco 24** · _tabela: Entrada Principal → Mesa 4 (valores reais)_  
Agora, um caso em que a heurística do projeto não ajuda nada: quando a origem é a própria Entrada Principal. Da entrada até a Mesa 4, os dois algoritmos expandem os mesmos 4 nós.

**[00:36:53] Bloco 25** · _formula: _  
O motivo é matemático. Para um nó n que a busca alcança vindo da entrada, g de n é igual à distância da entrada até n. Então f igual a g mais o destino menos g dá sempre o mesmo valor.

**[00:37:06] Bloco 26** · _topicos: Para a defesa_  
Isso explica o experimento da Fase 1, que mede tudo a partir da entrada. Guarde esse ponto para a defesa: não é erro de implementação, é a escolha do ponto de referência.

**[00:37:17] Bloco 27** · _topicos: Complexidade_  
Sobre complexidade: cada ligação pode colocar um item na fronteira, e a cada volta `min` e `remove` percorrem a fronteira inteira. No pior caso, isso dá algo da ordem de E ao quadrado, onde E é o número de ligações.

**[00:37:31] Bloco 28** · _topicos: Complexidade_  
Com `heapq` e um conjunto para os visitados, cairia para E vezes log de E. Mas com 90 ligações, a versão simples resolve cada busca em centésimos de milissegundo, e é bem mais fácil de explicar.

## Capítulo 8 — Ferramentas e experimento da Fase 1  (início 00:37:45, duração 00:05:19)

**[00:37:45] Bloco 1** · _titulo: Ferramentas e experimento da Fase 1_  
Capítulo oito. Com a busca pronta, o projeto cria funções de uso direto e faz o experimento comparativo pedido no Marco 1.

**[00:37:53] Bloco 2** · _código: célula 7, linhas 56–63_  
Comece por `calcular_tempo`. Ela recebe a distância em metros e a velocidade em quilômetros por hora, e devolve segundos. Antes da conta, ela confere os dados.

**[00:38:05] Bloco 3** · _código: célula 7, linhas 57–57_  
A primeira conferência: a velocidade precisa ser `int` ou `float`. `isinstance` testa o tipo; passar uma tupla de tipos aceita qualquer um deles.

**[00:38:15] Bloco 4** · _código: célula 7, linhas 57–57_  
Por que rejeitar `bool` à parte? Porque em Python `True` é um tipo especial de `int` e valeria 1. Sem esse teste, `calcular_tempo(10, True)` funcionaria e daria um resultado sem sentido.

**[00:38:27] Bloco 5** · _código: célula 7, linhas 59–62_  
Depois, a velocidade precisa ser maior que zero e finita, e a distância não pode ser negativa. Comparações encadeadas como `0 < v < inf` são válidas em Python. `float("inf")` é o infinito.

**[00:38:40] Bloco 6** · _código: célula 9, linhas 1–1_  
Agora `calcular_rota`, na seção 4. Repare nas anotações de tipo: `origem: str` e `-> str`, com uma seta. Elas não mudam a execução; documentam que a função recebe e devolve texto.

**[00:38:54] Bloco 7** · _código: célula 9, linhas 2–8_  
O texto entre aspas triplas logo abaixo do `def` é a docstring. Com a linha `Args:` e uma linha por parâmetro, ela segue o formato do gabarito: é o que o modelo de linguagem lê sobre uma ferramenta.

**[00:39:07] Bloco 8** · _código: célula 9, linhas 9–15_  
A função confere se os locais existem, valida a velocidade chamando `calcular_tempo` com zero metros dentro de um `try`, e só então chama `a_estrela`.

**[00:39:16] Bloco 9** · _código: célula 9, linhas 16–17_  
Se `a_estrela` devolver `None`, não há caminho, e a função avisa com um texto, em vez de tentar calcular o tempo de um caminho que não existe.

**[00:39:25] Bloco 10** · _código: célula 9, linhas 18–22_  
No fim, monta o texto de resposta. `" -> ".join(caminho)` junta os nomes com uma seta entre eles. Nas f-strings, `:.1f` mostra uma casa decimal e `:g` mostra o número sem zeros desnecessários.

**[00:39:39] Bloco 11** · _código: célula 11, linhas 1–4 | terminal: Saída real da seção 5_  
Esta é a saída real da seção 5, que chama `calcular_rota` para quatro consultas. Da entrada até a Mesa 4: 89,5 metros e 21,5 segundos, a 15 quilômetros por hora, sem paradas.

**[00:39:54] Bloco 12** · _terminal: Saída real da seção 5_  
Este tempo é ideal: só distância dividida por velocidade. Ele não é o tempo previsto da Fase 2 e não é exposto ao Qwen: serve como referência do Marco 1.

**[00:40:05] Bloco 13** · _código: célula 13, linhas 4–20_  
Agora o experimento. O enunciado pede comparar uma busca não informada com o A estrela em mapas de tamanhos diferentes. O projeto recorta o próprio campus em 20, 40 e 70 nós.

**[00:40:17] Bloco 14** · _código: célula 13, linhas 6–13_  
`recortar_mapa` é uma busca em largura: começa na entrada, usa uma fila, e a cada passo retira o primeiro da fila com `pop(0)` e acrescenta os vizinhos ainda não escolhidos.

**[00:40:29] Bloco 15** · _código: célula 13, linhas 14–20_  
Ela para ao atingir a quantidade pedida. Depois monta um grafo novo só com as ligações entre os nós selecionados, sem inventar ligações.

**[00:40:38] Bloco 16** · _código: célula 13, linhas 1–24_  
A célula começa importando `median`, do módulo `statistics`. Antes do laço, cria a lista vazia `RESULTADOS` e fixa 30 repetições por medida.

**[00:40:48] Bloco 17** · _código: célula 13, linhas 25–29_  
O laço do experimento recorta cada mapa e escolhe como destino o nó mais distante da entrada, com `max` e uma lambda.

**[00:40:56] Bloco 18** · _código: célula 13, linhas 30–40_  
Para cada algoritmo, roda uma vez de aquecimento fora da medição e depois 30 repetições, medindo cada uma com `perf_counter`. Guarda a mediana dos tempos, que resiste a picos ocasionais.

**[00:41:08] Bloco 19** · _código: célula 13, linhas 42–46_  
No fim, a célula imprime a tabela. As f-strings usam alinhamento: `:>3` alinha à direita em 3 posições e `:<14` alinha à esquerda em 14, para as colunas ficarem retas.

**[00:41:21] Bloco 20** · _tabela: Experimento da Fase 1 (execução local)_  
Estes são os resultados reais. Os custos são iguais entre os algoritmos, como deve ser. E os nós expandidos também são iguais: 19, 39 e 69.

**[00:41:33] Bloco 21** · _tabela: Experimento da Fase 1 (execução local)_  
Lembre do capítulo anterior: a origem é a Entrada, que é o ponto de referência da heurística. Por isso quase todos os nós empatam em f, e o A estrela não poupa expansões aqui.

**[00:41:44] Bloco 22** · _tabela: Experimento da Fase 1 (execução local)_  
O tempo do A estrela ficou um pouco maior, porque ele calcula a heurística para cada vizinho sem ganhar nada em troca. São centésimos de milissegundo, e variam entre máquinas.

**[00:41:56] Bloco 23** · _código: célula 16, linhas 3–26_  
A seção 5.2 desenha os gráficos com Matplotlib. Para cada métrica, `plt.bar` desenha as barras dos dois algoritmos lado a lado, deslocadas para a esquerda e para a direita.

**[00:42:08] Bloco 24** · _imagem: Gráfico real: nós expandidos_  
Este é o gráfico real de nós expandidos, gerado na execução do Colab.

**[00:42:13] Bloco 25** · _imagem: Gráfico real: tempo de execução (Colab)_  
E este é o do tempo de execução. No Colab, os tempos foram maiores que na máquina local, mas a relação se manteve: o A estrela um pouco mais lento nesse experimento.

**[00:42:24] Bloco 26** · _código: célula 16, linhas 28–42_  
A mesma célula desenha um último gráfico: o tempo ideal da Entrada até a Mesa 4, a 15 quilômetros por hora. A compreensão de lista na linha 31 chama `calcular_tempo` para cada velocidade da lista.

**[00:42:37] Bloco 27** · _imagem: Gráfico real: tempo ideal de deslocamento_  
O resultado real é este: 21,5 segundos para 89,5 metros, sem paradas. É a referência que a Fase 2 vai substituir pelo tempo previsto com atrasos.

**[00:42:50] Bloco 28** · _topicos: Limites do experimento_  
Uma limitação honesta para o relatório: os três mapas são recortes do mesmo campus, não mapas independentes, e há uma consulta por tamanho. Uma origem diferente da entrada mostraria a vantagem do A estrela, como vimos com a Mesa 1.

## Capítulo 9 — Fase 2: dados sintéticos e modelos de tempo  (início 00:43:04, duração 00:06:11)

**[00:43:04] Bloco 1** · _titulo: Fase 2: aprender o tempo de cada trecho_  
Capítulo nove: a Fase 2. Até aqui, o melhor caminho era o mais curto. Mas o mais curto nem sempre é o mais rápido. Agora o agente vai aprender, com dados, quanto tempo cada trecho leva.

**[00:43:18] Bloco 2** · _topicos: Os dados_  
O enunciado permite dados sintéticos, desde que documentados. O grupo gera uma tabela fictícia: para cada um dos 90 trechos, dois cenários e 12 repetições. São 2160 linhas.

**[00:43:33] Bloco 3** · _código: célula 19, linhas 16–18_  
Depois das importações, a célula fixa a semente em 42 e cria a pasta `resultados_fase2_15kmh` com `Path`. O `exist_ok=True` evita erro se a pasta já existir.

**[00:43:45] Bloco 4** · _código: célula 19, linhas 21–23_  
A geração fica em `gerar_dados_sinteticos`. `random.Random(SEMENTE_DADOS)` cria um sorteador com semente 42. A semente faz os sorteios saírem iguais em toda execução: o experimento é reproduzível.

**[00:44:00] Bloco 5** · _código: célula 19, linhas 24–27_  
Para cada trecho, o laço usa `enumerate` sobre `LIGACOES`, que dá o número do trecho e a tupla com origem, destino e distância. Piso e porta são sorteados uma vez por trecho.

**[00:44:12] Bloco 6** · _código: célula 19, linhas 28–31_  
Depois, para cada cenário e cada repetição, sorteia o fluxo de pessoas: de 0 a 2 no tranquilo, de 3 a 5 no movimentado. E um obstáculo, com 10 ou 40 por cento de chance.

**[00:44:25] Bloco 7** · _formula: A regra que gera o alvo_  
O tempo segue uma regra pública. A base é a distância a 15 quilômetros por hora. Ela cresce 15 por cento por unidade de fluxo e 25 por cento com piso irregular.

**[00:44:36] Bloco 8** · _código: célula 19, linhas 32–39_  
Uma porta soma 3 segundos, um obstáculo soma 12, e `gauss(0, 0.8)` acrescenta um ruído aleatório, para os dados não serem perfeitos. O `max(0.1, tempo)` impede tempo negativo.

**[00:44:50] Bloco 9** · _tabela: Primeiras linhas de DADOS_TEMPO (reais)_  
Cada linha vira um dicionário, e a lista de dicionários vira uma tabela do pandas, o DataFrame. Estas são as três primeiras linhas reais.

**[00:44:59] Bloco 10** · _tabela: Primeiras linhas de DADOS_TEMPO (reais)_  
Repare: o mesmo trecho, no mesmo cenário, tem tempos diferentes. A terceira linha teve um obstáculo e passou de 30 segundos. É essa variação que o modelo precisa aprender a prever em média.

**[00:45:13] Bloco 11** · _código: célula 19, linhas 65–70_  
Logo depois da geração, três `assert` conferem a tabela: nenhum valor faltando, nenhuma linha duplicada e todos os tempos positivos.

**[00:45:22] Bloco 12** · _código: célula 19, linhas 43–45_  
As entradas do modelo são separadas em numéricas, como distância, fluxo, porta e obstáculo, e categóricas, como piso e cenário. Nomes de locais e o número do trecho não entram.

**[00:45:34] Bloco 13** · _código: célula 19, linhas 48–49_  
`preparar_modelo` monta um Pipeline, uma sequência de etapas aplicadas em ordem. Para as numéricas: preencher faltantes com a mediana e padronizar a escala com `StandardScaler`.

**[00:45:45] Bloco 14** · _código: célula 19, linhas 50–51_  
Para as categóricas: preencher faltantes com o valor mais frequente e aplicar one-hot. One-hot transforma “regular” e “irregular” em colunas de zero e um, porque modelos só fazem contas com números.

**[00:45:58] Bloco 15** · _código: célula 19, linhas 52–56_  
O `ColumnTransformer` aplica cada preparo à sua lista de colunas. E o estimador no fim é uma regressão linear ou uma árvore de decisão, conforme o nome.

**[00:46:08] Bloco 16** · _topicos: Por que um Pipeline_  
Por que o Pipeline? Porque o preparo aprende valores, como médias e medianas. Dentro do Pipeline, ele aprende só com os dados de treino de cada rodada, e nada do teste vaza para o treino.

**[00:46:20] Bloco 17** · _topicos: Os dois modelos_  
A regressão linear supõe que o tempo é uma soma de pesos vezes atributos. A árvore de decisão divide os dados em perguntas sucessivas, com profundidade máxima 8 e pelo menos 5 linhas por folha.

**[00:46:33] Bloco 18** · _código: célula 19, linhas 72–76_  
Agora a divisão dos dados. `GroupShuffleSplit` separa 20 por cento dos trechos para teste. A palavra-chave é trecho: todas as linhas de um trecho ficam do mesmo lado.

**[00:46:44] Bloco 19** · _código: célula 19, linhas 76–76_  
Por que agrupar? Se o mesmo trecho aparecesse no treino e no teste, o modelo seria testado com algo muito parecido com o que já viu, e o erro pareceria menor do que é.

**[00:46:55] Bloco 20** · _código: célula 19, linhas 77–82_  
Nos trechos de treino, os dois modelos passam por validação cruzada com `GroupKFold` de 5 grupos. `cross_val_predict` treina em 4 partes e prevê a quinta, girando até todas serem previstas.

**[00:47:08] Bloco 21** · _código: célula 19, linhas 59–62_  
As métricas: MAE é o erro absoluto médio, em segundos. RMSE é a raiz do erro quadrático médio, que pune mais os erros grandes. E R² mede quanto da variação o modelo explica, de 0 a 1.

**[00:47:24] Bloco 22** · _tabela: Validação cruzada por trecho (5 grupos)_  
Resultado real da validação: a regressão linear errou 0,85 segundo em média, e a árvore, 1,0. A linear também venceu no RMSE e no R².

**[00:47:36] Bloco 23** · _tabela: Validação cruzada por trecho (5 grupos)_  
Faz sentido: a regra que gerou os dados é quase uma soma de termos, exatamente o formato da regressão linear. Num campus real, com relações mais complicadas, a árvore poderia ganhar.

**[00:47:48] Bloco 24** · _código: célula 19, linhas 83–87_  
`min` com uma lambda escolhe o modelo de menor MAE. Ele é treinado no conjunto de treino e avaliado uma única vez no teste reservado.

**[00:47:57] Bloco 25** · _tabela: Teste reservado (usado uma vez, depois da escolha)_  
No teste, a regressão linear teve MAE de 0,84 segundo, RMSE de 1,16 e R² de 0,97. O resultado é parecido com a validação, sinal de que não houve sobreajuste.

**[00:48:12] Bloco 26** · _terminal: Cinco maiores erros no teste (saída real)_  
O notebook também mostra onde o modelo erra mais. Os cinco maiores erros do teste estão todos num trecho longo, Entrada até Eixo Norte, com 60 metros, chegando a 5,8 segundos.

**[00:48:26] Bloco 27** · _topicos: Onde e por que erra_  
Por quê? Na regra, fluxo e piso multiplicam a base, e a base é maior em trechos longos. A regressão linear soma efeitos e não modela bem essa multiplicação. É uma análise honesta de onde o modelo erra.

**[00:48:40] Bloco 28** · _código: célula 19, linhas 88–101_  
Essa análise vem destas linhas. A tabela `erros` copia o teste e ganha as colunas de previsão e de erro absoluto. `groupby` calcula o erro médio por cenário, e `nlargest` pega os cinco maiores.

**[00:48:53] Bloco 29** · _código: célula 19, linhas 91–106_  
Os resultados são gravados em arquivos: as previsões e a validação em CSV, e um resumo em JSON, com a semente, os trechos de treino e teste e as métricas. Isso documenta a execução.

**[00:49:06] Bloco 30** · _código: célula 19, linhas 108–110_  
Por fim, o modelo é treinado de novo com todos os dados, para uso da ferramenta. As métricas relatadas são as de antes desse retreino.

## Capítulo 10 — Fase 2: o custo aprendido entra na busca  (início 00:49:16, duração 00:04:15)

**[00:49:16] Bloco 1** · _titulo: O custo aprendido entra na busca_  
Capítulo dez. O modelo de tempo está treinado. Agora vem o elo entre as fases: a mesma busca A estrela passa a usar o tempo previsto como custo de cada ligação.

**[00:49:27] Bloco 2** · _código: célula 19, linhas 113–115_  
`prever_grafo_tempo` recebe um cenário e devolve um grafo novo, com o mesmo formato de `VIZINHOS`, mas com segundos no lugar de metros. Primeiro, confere se o cenário existe.

**[00:49:38] Bloco 3** · _código: célula 19, linhas 116–120_  
Ela pega uma linha por trecho com `drop_duplicates`, e preenche os atributos do cenário: no tranquilo, fluxo 1 e sem obstáculo; no movimentado, fluxo 4 e com obstáculo.

**[00:49:50] Bloco 4** · _código: célula 19, linhas 121–125_  
O terceiro cenário, cadeiras no pátio, é didático. Ele parte do tranquilo, mas no trecho entre Pátio A e Pátio B coloca fluxo 5, obstáculo e cenário movimentado.

**[00:50:02] Bloco 5** · _código: célula 19, linhas 124–124_  
A comparação `{origem, destino} == {"Pátio - A", "Pátio - B"}` usa conjuntos: assim não importa a ordem em que os dois nomes aparecem na ligação.

**[00:50:12] Bloco 6** · _código: célula 19, linhas 126–127_  
Então o modelo prevê o tempo dos 90 trechos de uma vez, com `predict`. O `np.maximum(0.1, ...)` garante que nenhum tempo seja menor que um décimo de segundo.

**[00:50:23] Bloco 7** · _código: célula 19, linhas 128–132_  
Por fim, monta o dicionário do grafo nos dois sentidos, como na seção 2. `zip` percorre as ligações e os tempos previstos lado a lado.

**[00:50:32] Bloco 8** · _grafo do campus_  
Veja o pátio no cenário tranquilo, com os tempos previstos reais em segundos. A ligação de A até B leva 9,7 segundos.

**[00:50:42] Bloco 9** · _grafo do campus_  
No cenário cadeiras no pátio, a mesma ligação passa para 23 segundos. As outras continuam iguais.

**[00:50:50] Bloco 10** · _código: célula 19, linhas 135–145_  
Agora a ferramenta usada pelo agente: `rota_tempo_previsto`. A docstring diz ao modelo de linguagem para que ela serve e o que significa cada parâmetro, inclusive as três opções de cenário.

**[00:51:03] Bloco 11** · _código: célula 19, linhas 146–152_  
Ela valida os locais e o cenário, gera o grafo de tempos, e recalcula a tabela de referência da heurística, agora em segundos, com uma compreensão de dicionário.

**[00:51:13] Bloco 12** · _código: célula 19, linhas 153–153_  
A busca é a mesma `buscar` da Fase 1, com a heurística ligada. Só mudaram o grafo e a referência. Esse é o ponto central da Fase 2.

**[00:51:23] Bloco 13** · _código: célula 19, linhas 154–155_  
Se não houver caminho, a função devolve um aviso em texto.

**[00:51:27] Bloco 14** · _código: célula 19, linhas 156–156_  
A distância informada é a soma dos metros da rota escolhida por tempo. `dict(VIZINHOS[a])[b]` transforma a lista de vizinhos num dicionário para achar os metros de cada passo.

**[00:51:38] Bloco 15** · _código: célula 19, linhas 157–163_  
E a resposta é um texto com caminho, distância, tempo previsto, a base fixa e avisos de que os dados são sintéticos.

**[00:51:46] Bloco 16** · _código: célula 19, linhas 166–167_  
Logo depois da definição, um `for` chama a ferramenta para a consulta padrão nos dois cenários.

**[00:51:52] Bloco 17** · _terminal: rota_tempo_previsto("Entrada Principal", "Mesa 4", "tranquilo") / terminal: rota_tempo_previsto("Entrada Principal", "Mesa 4", "movimentado")_  
Saídas reais da Entrada até a Mesa 4: no tranquilo, 30 segundos; no movimentado, 68,9 segundos, pelo mesmo caminho de 89,5 metros.

**[00:52:05] Bloco 18** · _código: célula 19, linhas 170–185_  
Agora a demonstração mais importante para a apresentação: `demonstrar_alternativa_patio`. Ela compara a rota mais curta e a rota mais rápida da Mesa 1 até a Mesa 4, com cadeiras no pátio.

**[00:52:17] Bloco 19** · _código: célula 19, linhas 171–188_  
Ela calcula a rota mais curta com `a_estrela`, a rota mais rápida com `buscar` no grafo de tempos, mede o tempo da rota curta no grafo de tempos e grava tudo num JSON. A linha 188 guarda o resultado em `DEMONSTRACAO_PATIO`.

**[00:52:32] Bloco 20** · _grafo do campus_  
A rota mais curta, em metros, passa por Pátio B: 42 metros. Mas com cadeiras, o trecho de A até B demora. Somando os tempos previstos, essa rota leva 35,7 segundos.

**[00:52:46] Bloco 21** · _grafo do campus (caminho Mesa 1 → Pátio - A → Pátio - D → Pátio/Direito → Mesa 4; carrinho animado)_  
O A estrela, com custo em segundos, escolhe outro caminho: por Pátio D. São 46 metros, quatro a mais, mas só 23,7 segundos.

**[00:52:57] Bloco 22** · _tabela: Mesa 1 → Mesa 4 com cadeiras no pátio (valores reais)_  
A economia prevista é de 12 segundos. Este é o modelo de custo mudando a decisão da busca, exatamente o que o enunciado pede para mostrar na demonstração ao vivo.

**[00:53:08] Bloco 23** · _topicos: Limites da Fase 2_  
Vale lembrar o limite: o programa não detecta cadeiras de verdade. O cenário é uma hipótese digitada no pedido, e os tempos são sintéticos. É isso que o relatório deve dizer.

**[00:53:21] Bloco 24** · _código: célula 19, linhas 190–190_  
A célula termina com `FERRAMENTAS = [rota_tempo_previsto, listar_vizinhos]`: a lista das duas funções que o Qwen poderá chamar. É a ponte para a Fase 3.

## Capítulo 11 — Fase 3: o Qwen e as ferramentas  (início 00:53:31, duração 00:04:50)

**[00:53:31] Bloco 1** · _titulo: Fase 3: o modelo de linguagem_  
Capítulo onze: a Fase 3. Um modelo de linguagem passa a receber os pedidos em português. Primeiro, vamos entender como ele é carregado e como “enxerga” as ferramentas.

**[00:53:43] Bloco 2** · _topicos: O papel do LLM_  
O papel do modelo é muito claro no enunciado: ele não calcula a rota. Modelos de linguagem são bons com linguagem, e ruins com contas exatas de caminhos. Ele entende o pedido, chama a ferramenta e explica.

**[00:53:57] Bloco 3** · _código: célula 22, linhas 1–9_  
A seção 6 começa importando `torch`, o PyTorch, e duas classes da biblioteca transformers. Depois verifica se há placa de vídeo: `torch.cuda.is_available()` devolve verdadeiro se houver GPU.

**[00:54:10] Bloco 4** · _código: célula 22, linhas 11–11_  
O modelo é o Qwen2.5-1.5B-Instruct: 1,5 bilhão de parâmetros, treinado para seguir instruções. É público e roda dentro da própria sessão, sem chave de API e sem custo por chamada.

**[00:54:24] Bloco 5** · _código: célula 22, linhas 12–16_  
O tokenizador converte texto em números, os tokens, que são pedaços de palavras. O modelo só trabalha com esses números. `from_pretrained` baixa e carrega os dois na primeira execução.

**[00:54:37] Bloco 6** · _código: célula 22, linhas 13–17_  
Com GPU, o modelo usa `float16`, metade da memória, e vai para a placa com `.to(dispositivo)`. Sem GPU, usa `float32` na CPU. E `qwen.eval()` coloca o modelo em modo de uso, sem treino.

**[00:54:53] Bloco 7** · _código: célula 22, linhas 23–24_  
Agora a função `conversar`. Ela recebe a lista de mensagens, a lista de ferramentas e o limite de tokens. `global ULTIMA_GERACAO` permite registrar informações da última geração.

**[00:55:05] Bloco 8** · _código: célula 22, linhas 25–28_  
`apply_chat_template` monta o texto no formato que o Qwen foi treinado para ler: as mensagens com seus papéis e a descrição das ferramentas. `add_generation_prompt` avisa que agora é a vez do assistente.

**[00:55:17] Bloco 9** · _código: célula 22, linhas 27–28_  
`return_tensors="pt"` devolve os números como tensores do PyTorch, e `.to(dispositivo)` os coloca no mesmo lugar do modelo.

**[00:55:25] Bloco 10** · _código: célula 22, linhas 29–30_  
`torch.no_grad()` desliga o cálculo de gradientes, que só serve para treinar, e economiza memória. `generate` produz até `max_tokens` tokens novos. E `do_sample=False` escolhe sempre o token mais provável.

**[00:55:40] Bloco 11** · _código: célula 22, linhas 30–30_  
Por isso as execuções no Colab e na máquina local deram exatamente os mesmos acertos: com `do_sample` falso, a mesma entrada gera a mesma saída.

**[00:55:49] Bloco 12** · _código: célula 22, linhas 31–32_  
A saída do `generate` contém a pergunta e a resposta juntas. A fatia `saida[0][tamanho_da_pergunta:]` corta a parte da pergunta e deixa só os tokens novos.

**[00:56:00] Bloco 13** · _código: célula 22, linhas 33–37_  
As linhas seguintes registram por que a geração terminou: `eos` se o modelo encerrou sozinho, ou limite de tokens se foi cortado. Isso ajuda a diagnosticar respostas incompletas.

**[00:56:11] Bloco 14** · _código: célula 22, linhas 38–38_  
Por fim, `decode` transforma os números de volta em texto, pulando os tokens especiais.

**[00:56:17] Bloco 15** · _código: célula 26, linhas 1–3 | terminal: get_json_schema(rota_tempo_previsto) · resumo da saída real_  
Como o modelo conhece as ferramentas? Ele nunca vê o código Python. A biblioteca transforma cada função numa ficha em JSON, com nome, descrição e parâmetros, tirados das anotações de tipo e da docstring.

**[00:56:32] Bloco 16** · _terminal: get_json_schema(rota_tempo_previsto) · resumo da saída real_  
Repare que a lista de opções do cenário virou um `enum`, e que origem e destino são obrigatórios. Por isso a docstring precisa ser bem escrita: ela é a única coisa que o modelo lê sobre a ferramenta.

**[00:56:44] Bloco 17** · _fluxo: Como o Qwen recebe a conversa_  
A conversa é uma lista de mensagens com papéis. `system` traz as regras do agente; `user` traz a pergunta. O modelo responde como `assistant`.

**[00:56:55] Bloco 18** · _fluxo: Como o Qwen recebe a conversa_  
Quando decide usar uma ferramenta, o modelo não executa nada. Ele só escreve um texto especial entre as marcas `tool_call`, com o nome da ferramenta e os argumentos em JSON.

**[00:57:06] Bloco 19** · _código: célula 24, linhas 144–150_  
As regras ficam na variável `REGRAS`, na seção 7. É o prompt do sistema, e ele é versionado: os comentários registram o que mudou da versão 1 até a 5, e por quê.

**[00:57:17] Bloco 20** · _código: célula 24, linhas 151–153_  
Repare na sintaxe: `REGRAS` é uma única string, escrita em várias linhas. Dentro de parênteses, strings vizinhas são juntadas automaticamente pelo Python, sem precisar do sinal de mais.

**[00:57:31] Bloco 21** · _código: célula 24, linhas 152–157_  
As primeiras frases dizem que o Qwen não conhece o mapa nem os tempos, e que deve chamar uma ferramenta sempre que a pergunta citar um local. Isso entrou na versão 5, depois de um teste real.

**[00:57:43] Bloco 22** · _código: célula 24, linhas 147–149_  
Na versão 4, o Qwen respondeu 15 de 39 pedidos sem chamar ferramenta, inventando rotas e números como 78 metros. Foi a avaliação real que mostrou o problema.

**[00:57:55] Bloco 23** · _código: célula 24, linhas 158–165_  
Outras regras pedem para copiar os nomes como o usuário escreveu, sem trocar origem e destino, e explicam os cenários. Há até um exemplo: “biblio para b4” usa origem biblio e destino b4.

**[00:58:08] Bloco 24** · _código: célula 24, linhas 166–171_  
E as últimas frases pedem para explicar o resultado só depois de recebê-lo, copiando os números como vieram, sem converter unidades. No próximo capítulo, veremos como o código confere o pedido do modelo.

## Capítulo 12 — Fase 3: o código confere o pedido do modelo  (início 00:58:21, duração 00:06:31)

**[00:58:21] Bloco 1** · _titulo: O código confere o pedido_  
Capítulo doze. O Qwen escreve um pedido de ferramenta. Mas um modelo pequeno erra: troca nomes, inventa locais, usa cenários errados. Por isso, antes de executar, o código confere tudo.

**[00:58:35] Bloco 2** · _código: célula 24, linhas 2–9_  
A seção 7 importa `json`, `re`, `unicodedata` e `get_close_matches`, todos nativos do Python. Depois cria a tabela `TROCAS`, um dicionário de palavras a trocar ou ignorar.

**[00:58:48] Bloco 3** · _código: célula 24, linhas 12–25_  
A primeira peça é `padronizar`. Ela transforma qualquer texto numa forma simples e comparável, para que “Sala B04”, “b4” e “B-04” virem a mesma coisa.

**[00:58:59] Bloco 4** · _código: célula 24, linhas 14–15_  
Passo um: `lower()` deixa tudo minúsculo. `unicodedata.normalize` com a forma NFD separa cada letra do seu acento, e a linha 15 descarta os acentos, que têm a categoria Mn.

**[00:59:12] Bloco 5** · _código: célula 24, linhas 16–17_  
Passo dois, com expressões regulares: `re.sub` troca tudo o que não é letra ou número por espaço. E a linha 17 coloca um espaço entre letra e número: b4 vira b espaço 4.

**[00:59:25] Bloco 6** · _código: célula 24, linhas 18–25_  
Passo três: para cada palavra, a tabela `TROCAS` substitui ou apaga. Banheiro vira wc, fem vira feminino, e palavras como sala, bloco, do e da somem. Números perdem zeros à esquerda com `int`.

**[00:59:39] Bloco 7** · _transformacao: `padronizar("Sala B04")`_  
Veja a transformação real de “Sala B04”, passo a passo, até chegar em “b 4”.

**[00:59:45] Bloco 8** · _transformacao: `padronizar("Sala B04")`_  
A sala some, porque está na tabela de palavras ignoradas, e o zero de 04 também. É por isso que “B-04” e “Sala B04” chegam ao mesmo nome padronizado.

**[00:59:57] Bloco 9** · _tabela: padronizar: exemplos reais_  
Mais dois exemplos reais: “banheiro fem do Design” vira “wc feminino design”, igual ao nome padronizado de “WC Feminino Design”. E “Pátio/Direito” vira “patio direito”.

**[01:00:09] Bloco 10** · _código: célula 24, linhas 39–45_  
Com isso, o código monta o dicionário `NOMES`: a chave é o nome padronizado, e o valor é o nome oficial do mapa. O `assert` garante que dois locais nunca fiquem com o mesmo nome padronizado.

**[01:00:20] Bloco 11** · _código: célula 24, linhas 28–37_  
Os apelidos também entram em `NOMES`: biblio leva à Biblioteca, mesa um leva à Mesa 1. Já os genéricos, como banheiro e lanchonete, ficam em outro dicionário, porque apontam para vários locais.

**[01:00:34] Bloco 12** · _código: célula 24, linhas 47–49_  
E o dicionário `CENARIOS` lista, para cada cenário, as palavras que o usuário pode usar: lotado e cheio indicam movimentado; calmo e normal indicam tranquilo.

**[01:00:44] Bloco 13** · _fluxo: resolver_local: a ordem das perguntas_  
Agora `resolver_local`, que decide qual local o texto significa. Ela devolve uma tupla: o local, ou `None`, e uma lista de opções.

**[01:00:53] Bloco 14** · _fluxo: resolver_local: a ordem das perguntas_  
Primeiro, procura o texto padronizado em `NOMES`. Se achar, é um nome do mapa ou um apelido, e devolve o local.

**[01:01:01] Bloco 15** · _fluxo: resolver_local: a ordem das perguntas_  
Se for genérico, devolve `None` com a lista de opções, para o programa perguntar qual. Para banheiro, são 13 opções; para lanchonete, Easy Smart e Café Mania.

**[01:01:12] Bloco 16** · _fluxo: resolver_local: a ordem das perguntas_  
Se o texto tiver número ou estiver vazio, devolve `None` sem opções. Uma decisão de segurança: “B-07” não existe, e o código nunca “corrige” para uma sala parecida, como B-01.

**[01:01:25] Bloco 17** · _fluxo: resolver_local: a ordem das perguntas_  
Só então tenta erro de digitação com `get_close_matches`, que compara a semelhança entre textos. O corte de 0,85 exige muita semelhança, e o resultado só é aceito se houver um único candidato.

**[01:01:38] Bloco 18** · _código: célula 24, linhas 52–64_  
No código, são poucas linhas, na mesma ordem do diagrama.

**[01:01:42] Bloco 19** · _tabela: resolver_local: exemplos reais_  
Exemplos reais: “b4” e “biblio” são resolvidos direto; “bibliotca” e “cafe manai” por semelhança; banheiro e lanchonete pedem escolha; sala 02, B-07 e auditório pedem um nome do mapa.

**[01:01:56] Bloco 20** · _código: célula 24, linhas 67–73 | tabela: resolver_cenario (real)_  
`resolver_cenario` faz o mesmo com os cenários. Lotado vira movimentado, e até grafias erradas como “tranqulho” e “tranq” viram tranquilo, por causa do corte menor, de 0,7.

**[01:02:08] Bloco 21** · _código: célula 24, linhas 76–78_  
Duas funções conferem se o modelo não inventou nada. `aparece_na_pergunta` testa se alguma das palavras aparece no texto padronizado da pergunta.

**[01:02:18] Bloco 22** · _código: célula 24, linhas 81–90_  
E `local_na_pergunta` percorre todos os trechos de 1 a 4 palavras da pergunta e resolve cada um. Se algum trecho leva ao mesmo local que o modelo pediu, o local veio mesmo do usuário.

**[01:02:30] Bloco 23** · _tabela: local_na_pergunta (real)_  
Exemplo real: na pergunta “cafe manai para easy smrt”, o trecho “cafe manai” resolve para Café Mania, então o pedido é aceito. Já Mesa 3 não aparece em “da biblioteca para o banheiro”.

**[01:02:42] Bloco 24** · _código: célula 24, linhas 93–97_  
`pergunta_ao_usuario` monta o texto de esclarecimento. Se houver opções, lista as opções; senão, pede um nome do mapa com o exemplo B-04. A f-string coloca o nome do campo na pergunta.

**[01:02:55] Bloco 25** · _código: célula 24, linhas 100–100_  
`CAMPOS` diz quais argumentos de local cada ferramenta tem: origem e destino para a rota, e local para os vizinhos.

**[01:03:02] Bloco 26** · _código: célula 24, linhas 103–105_  
Tudo isso é reunido em `preparar_pedido`. Ela devolve um dicionário com um status: ok, se pode executar; erro, que volta para o modelo corrigir; ou esclarecimento, que vira uma pergunta ao usuário.

**[01:03:15] Bloco 27** · _código: célula 24, linhas 106–108_  
Primeiro, confere se o pedido é um dicionário com uma ferramenta conhecida. `pedido.get("name")` busca a chave sem dar erro se ela não existir.

**[01:03:25] Bloco 28** · _código: célula 24, linhas 109–110_  
Depois, parâmetros extras: a diferença entre conjuntos com o sinal de menos mostra o que sobrou. Se o modelo mandar velocidade, o pedido é recusado, porque a base é fixa.

**[01:03:36] Bloco 29** · _código: célula 24, linhas 111–120_  
Para cada campo de local, resolve o texto. Se não houver local, devolve esclarecimento. Se houver, mas não estiver na pergunta, devolve erro: o modelo inventou.

**[01:03:48] Bloco 30** · _código: célula 24, linhas 121–130_  
Para a rota, resolve o cenário. Se for diferente de tranquilo e não aparecer na pergunta, devolve erro com uma dica do cenário que o usuário citou.

**[01:03:57] Bloco 31** · _terminal: preparar_pedido · exemplo real_  
Exemplos reais. “biblio para b4”: o pedido vira Biblioteca até B-04, cenário tranquilo, status ok.

**[01:04:06] Bloco 32** · _terminal: preparar_pedido · exemplo real_  
“da biblioteca para o banheiro”: status esclarecimento, com a pergunta “Qual é o local de destino?” e as 13 opções de banheiro.

**[01:04:14] Bloco 33** · _terminal: preparar_pedido · exemplo real_  
Um pedido com velocidade 10 é recusado por parâmetro extra.

**[01:04:19] Bloco 34** · _terminal: preparar_pedido · exemplo real_  
E este caso aconteceu de verdade no teste: o usuário pediu cadeiras no pátio, e o Qwen mandou movimentado. O código recusa e devolve a dica: use cadeiras no pátio.

**[01:04:30] Bloco 35** · _código: célula 24, linhas 133–141_  
Por fim, `executar` chama `preparar_pedido` e, se estiver tudo certo, chama a função Python da ferramenta, desempacotando os argumentos com dois asteriscos.

**[01:04:40] Bloco 36** · _código: célula 24, linhas 140–140_  
Dois asteriscos transformam um dicionário em argumentos nomeados: origem igual a Biblioteca, destino igual a B-04, cenário igual a tranquilo. No próximo capítulo, o ciclo completo do agente.

## Capítulo 13 — Fase 3: o ciclo do agente e as interfaces  (início 01:04:53, duração 00:05:47)

**[01:04:53] Bloco 1** · _titulo: O ciclo do agente_  
Capítulo treze: a função `agente`, o coração da Fase 3. Ela segue o mesmo ciclo do gabarito da Aula 10: pensar, agir, observar e responder.

**[01:05:03] Bloco 2** · _fluxo: O ciclo da função `agente`_  
Pensar: o Qwen lê a conversa e decide se precisa de uma ferramenta.

**[01:05:08] Bloco 3** · _fluxo: O ciclo da função `agente`_  
Agir: o código confere o pedido e executa a ferramenta. Observar: o resultado volta para o Qwen como uma mensagem com o papel tool.

**[01:05:17] Bloco 4** · _fluxo: O ciclo da função `agente`_  
Responder: quando o Qwen não pede mais ferramenta, o texto dele é a resposta final. O ciclo tem no máximo 3 passos, para não girar para sempre.

**[01:05:27] Bloco 5** · _código: célula 24, linhas 183–191_  
Antes do ciclo, três funções auxiliares. `extrair_json` procura a primeira chave aberta e a última chave fechada do texto, e tenta converter o trecho com `json.loads`.

**[01:05:39] Bloco 6** · _código: célula 24, linhas 188–191_  
Se o texto não for JSON válido, `json.loads` dispara `ValueError`, e o `except` devolve `None`. Assim um JSON quebrado não derruba o programa.

**[01:05:49] Bloco 7** · _código: célula 24, linhas 194–198_  
`ler_pedido_de_ferramenta` só tenta ler um pedido se houver a marca tool_call ou se o texto começar com chave. Essa segunda condição entrou depois do teste real: o Qwen pequeno às vezes esquece as marcas.

**[01:06:01] Bloco 8** · _código: célula 24, linhas 173–180 | tabela: fala_do_mapa (real)_  
`fala_do_mapa` diz se a pergunta cita um local, um nome genérico ou uma palavra de rota. Resultados reais: “Bom dia!” dá falso; “mesa 1 pra lanchonete” dá verdadeiro.

**[01:06:13] Bloco 9** · _código: célula 24, linhas 201–208_  
`numeros_fora_da_ferramenta` é o controle de alucinação. Ela pega todos os números da explicação do Qwen e tira os que aparecem nos resultados das ferramentas. O que sobra foi inventado.

**[01:06:26] Bloco 10** · _código: célula 24, linhas 204–208 | terminal: numeros_fora_da_ferramenta (real)_  
Detalhes: marcadores de lista no início da linha são ignorados, e os números viram `float`, então 46 e 46.0 contam como iguais. Exemplo real: se o resultado diz 74.2 e o Qwen escreve 74, o 74 é sinalizado.

**[01:06:44] Bloco 11** · _código: célula 24, linhas 211–216_  
Agora a função `agente`. Ela monta a lista de mensagens: as regras como system, o histórico, se houver, e a pergunta como user.

**[01:06:52] Bloco 12** · _código: célula 24, linhas 215–216_  
A variável `contexto` junta o que o usuário escreveu, inclusive no histórico. É com ela que `preparar_pedido` confere se os nomes vieram do usuário. E `detalhes` guarda tudo o que aconteceu, para a avaliação.

**[01:07:05] Bloco 13** · _código: célula 24, linhas 218–221_  
O laço roda no máximo 3 vezes. Passo 1, pensar: `conversar` gera a resposta do Qwen, e ela é guardada nas tentativas. Depois, tenta ler um pedido de ferramenta.

**[01:07:18] Bloco 14** · _código: célula 24, linhas 223–231_  
Se não há pedido, a resposta seria final. Mas se a pergunta fala do mapa e nenhuma ferramenta foi chamada, o texto seria inventado. Então o código devolve a pergunta ao Qwen, com o formato exato do pedido.

**[01:07:32] Bloco 15** · _código: célula 24, linhas 226–231_  
Esse bloco foi a principal correção da versão 5. Na avaliação real, ele trocou rotas inventadas por uma resposta honesta: não consegui consultar o mapa.

**[01:07:43] Bloco 16** · _código: célula 24, linhas 232–234_  
Caso contrário, passo 4, responder: a resposta vira a final, com status concluído se alguma ferramenta foi chamada, ou resposta livre, como numa saudação. O `break` sai do laço.

**[01:07:55] Bloco 17** · _código: célula 24, linhas 236–240_  
Se há pedido, o código confere. JSON inválido vira um erro. Senão, `preparar_pedido` analisa o pedido com o contexto.

**[01:08:04] Bloco 18** · _código: célula 24, linhas 242–245_  
Se faltar informação, o próprio programa pergunta ao usuário e sai do laço. O Qwen não escolhe o banheiro por você.

**[01:08:12] Bloco 19** · _código: célula 24, linhas 247–252_  
Passo 2, agir: se o status é ok, `executar` roda a ferramenta, e a chamada é registrada. Se é erro, a mensagem de erro passa a ser o resultado, e volta ao modelo.

**[01:08:24] Bloco 20** · _código: célula 24, linhas 253–255_  
Com `mostrar` verdadeiro, que é o padrão, o agente imprime o pedido e o resultado da ferramenta. É assim que a demonstração mostra o que acontece por dentro.

**[01:08:34] Bloco 21** · _código: célula 24, linhas 257–259_  
Passo 3, observar: a resposta do Qwen entra como assistant, e o resultado entra como tool. Na próxima volta, o Qwen lê o resultado e escreve a explicação.

**[01:08:45] Bloco 22** · _código: célula 24, linhas 260–261_  
Repare no `else` depois do `for`, na linha 260. Ele só roda se o laço terminar sem `break`, ou seja, se os 3 passos acabarem sem resposta final.

**[01:08:56] Bloco 23** · _código: célula 24, linhas 263–271_  
No fim, se a resposta foi concluída, o código procura números inventados. Se encontrar, acrescenta um aviso de verificação e o resultado exato da ferramenta.

**[01:09:07] Bloco 24** · _código: célula 26, linhas 5–14_  
A seção 8 testa o agente. Primeiro imprime a ficha JSON da ferramenta. Depois percorre uma lista de quatro perguntas e chama `agente` em cada uma.

**[01:09:18] Bloco 25** · _terminal: Execução real da seção 8.2_  
Esta é uma execução real, com o Qwen na GPU. O Qwen pediu `rota_tempo_previsto` de Biblioteca até Mesa 3, o A estrela calculou 113,5 metros e 43 segundos, e o Qwen explicou em português.

**[01:09:32] Bloco 26** · _terminal: Execução real da seção 8.2_  
A explicação usou 43 segundos, e o resultado dizia 43.0. Como os números são comparados como valores, isso não é sinalizado como invenção.

**[01:09:44] Bloco 27** · _código: célula 30, linhas 1–9_  
A seção 8 também mostra como perguntar. A célula 8.2 tem uma caixa de texto do Colab, criada pelo comentário especial `#@param`. Se a caixa estiver vazia, `input` abre um campo para digitar.

**[01:09:58] Bloco 28** · _código: célula 31, linhas 1–9_  
A célula do chat só chama `conversa_interativa` se a caixa `ABRIR_CONVERSA` for marcada. Assim, o “Executar tudo” não para esperando digitação.

**[01:10:08] Bloco 29** · _código: célula 28, linhas 1–17_  
`conversa_interativa` repete com `while True`, lê a pergunta com `input`, e trata sair, cancelar e texto vazio. Depois chama o agente com o histórico.

**[01:10:18] Bloco 30** · _código: célula 28, linhas 18–20_  
O histórico guarda só as duas últimas trocas, com a fatia de menos 4. Assim, depois de “Qual é o local de destino?”, a resposta “Café Mania” é entendida junto com o pedido anterior.

**[01:10:30] Bloco 31** · _código: célula 39, linhas 1–8_  
E a última célula do notebook usa `input` puro: espera perguntas até alguém digitar sair, com o `pergunta.strip().lower()` que estudamos no capítulo três.

## Capítulo 14 — Avaliação real do agente  (início 01:10:40, duração 00:04:06)

**[01:10:40] Bloco 1** · _titulo: Avaliação real do agente_  
Capítulo catorze: a avaliação. O enunciado pede pelo menos 15 pedidos de teste, com o resultado esperado, medindo em quantos o agente acerta, e uma análise das falhas. O projeto tem 39.

**[01:10:55] Bloco 2** · _código: célula 33, linhas 1–5_  
Cada caso é uma tupla com três valores: a pergunta, o que o agente deve fazer, e os argumentos esperados. O que fazer pode ser o nome da ferramenta, `None` ou esclarecer.

**[01:11:06] Bloco 3** · _código: célula 33, linhas 6–23_  
A lista é organizada por grupos, com comentários: rotas com nomes exatos, vizinhos, perguntas sem ferramenta e os três cenários.

**[01:11:15] Bloco 4** · _código: célula 33, linhas 24–51_  
Depois vêm os testes difíceis: escrita informal, abreviações, erros de digitação, ordem invertida, e pedidos em que falta informação ou o local não existe. Nesses, o esperado é esclarecer.

**[01:11:28] Bloco 5** · _código: célula 33, linhas 55–59_  
Antes de chamar o Qwen, a célula confere os próprios casos: todo caso de ferramenta precisa executar sem erro. Isso evita testar o agente contra uma resposta esperada errada.

**[01:11:40] Bloco 6** · _código: célula 35, linhas 2–11_  
A função `o_que_o_agente_fez` traduz os detalhes devolvidos pelo agente para o mesmo formato do caso: esclarecer com o campo, o nome e os argumentos da ferramenta, ou nada.

**[01:11:50] Bloco 7** · _código: célula 35, linhas 14–30_  
O laço mede o tempo de cada pedido com `perf_counter`, compara a escolha e os argumentos, e verifica números inventados. Um caso só é certo se tudo estiver certo.

**[01:12:01] Bloco 8** · _código: célula 35, linhas 27–37_  
Cada caso imprime uma linha com certo ou ERRADO, a escolha esperada e a feita, os números inventados e o tempo. E o dicionário do caso entra na lista `AVALIACAO`.

**[01:12:12] Bloco 9** · _código: célula 35, linhas 22–22_  
A linha 22 tem um detalhe: `dict` com dois asteriscos junta o cenário padrão tranquilo com os argumentos esperados, porque o agente sempre preenche o cenário.

**[01:12:22] Bloco 10** · _código: célula 35, linhas 39–57_  
No fim, o pandas monta a tabela, calcula os totais e salva um CSV com a versão das regras no nome.

**[01:12:29] Bloco 11** · _tabela: Resultado da avaliação (regras v5, execução real)_  
Resultado real, com o Qwen dois ponto cinco: 31 de 39 casos certos. Em 30 casos que pediam uma ferramenta, 24 tiveram ferramenta e argumentos certos. E 4 explicações tiveram números sinalizados.

**[01:12:45] Bloco 12** · _tabela: Acertos por grupo de casos_  
Por grupo, o ponto fraco é claro: escrita informal, com 3 de 10. Saudações e perguntas fora do mapa acertaram todas.

**[01:12:54] Bloco 13** · _terminal: cafe manai para easy smrt · respostas brutas do Qwen_  
Vamos ver as falhas de verdade, com o texto bruto que o Qwen escreveu. Em “cafe manai para easy smrt”, nas três tentativas, ele escreveu a mesma frase, sem chamar a ferramenta.

**[01:13:07] Bloco 14** · _terminal: cafe manai para easy smrt · respostas brutas do Qwen_  
Repare que “caminha 203” não existe no mapa. Sem a proteção da versão 5, isso seria mostrado ao usuário como se fosse verdade. Com ela, o agente admite que não conseguiu.

**[01:13:19] Bloco 15** · _terminal: mesa um pra mesa quatro, ta lotado · respostas brutas_  
Em “mesa um pra mesa quatro, ta lotado”, o Qwen entendeu outra coisa: que a mesa estava ocupada. Depois escreveu algo parecido com argumentos, mas fora do formato de ferramenta.

**[01:13:31] Bloco 16** · _terminal: O que há ao lado do Corredor Design? · respostas brutas_  
E em “O que há ao lado do Corredor Design?”, ele primeiro inventou salas 203, 204 e 205, e na segunda tentativa chamou a ferramenta de rota sem destino, quando o certo era listar vizinhos.

**[01:13:45] Bloco 17** · _topicos: Números sinalizados (todos arredondamentos)_  
As quatro explicações sinalizadas arredondaram números: 74,2 segundos virou 74, 51,8 virou 51, 22,2 virou 22 e 17,8 virou 17. A verificação pegou todas e mostrou o resultado exato.

**[01:14:04] Bloco 18** · _tabela: Versões das regras (execuções reais)_  
A comparação entre versões mostra o efeito das correções. Na versão 4, eram 24 certos, e 15 pedidos com rotas inventadas. Na versão 5, 31 certos e nenhuma rota inventada chegou ao usuário.

**[01:14:19] Bloco 19** · _tabela: Tempo por pedido (mesmo resultado nos dois)_  
Agora o custo. O Qwen roda dentro da sessão, sem API paga e sem chave no código. Mas não é de graça: cada pedido consome tempo de processamento e memória.

**[01:14:31] Bloco 20** · _topicos: Limites para o relatório_  
Na CPU, cada pedido levou cerca de 35 vezes mais. Por isso, na apresentação, é obrigatório escolher a GPU T4 no Colab. E pedidos com falha custam mais, porque o agente chama o Qwen até três vezes.

## Capítulo 15 — Simulação completa: do “Executar tudo” à resposta  (início 01:14:46, duração 00:02:42)

**[01:14:46] Bloco 1** · _titulo: Simulação completa_  
Capítulo quinze. Vamos juntar tudo e acompanhar o programa inteiro, do “Executar tudo” até a resposta de uma pergunta. Todos os valores são de execuções reais.

**[01:14:57] Bloco 2** · _cartoes: Memória da sessão_  
Ao clicar em executar tudo, a seção 1 cria as constantes: origem Entrada Principal, destino Mesa 4 e velocidade base 15.

**[01:15:06] Bloco 3** · _cartoes: Memória da sessão_  
A seção 2 constrói o grafo: `LOCAIS`, `LIGACOES` e `VIZINHOS`, e imprime 90 nós e 90 ligações.

**[01:15:13] Bloco 4** · _cartoes: Memória da sessão_  
A seção 3 define `buscar` e calcula `DISTANCIA_ENTRADA` para os 90 locais, em cerca de 3 milissegundos. As seções 4 e 5 criam as ferramentas e rodam o experimento.

**[01:15:26] Bloco 5** · _cartoes: Memória da sessão_  
A seção 5.3 gera 2160 linhas sintéticas, valida os dois modelos, escolhe a regressão linear e treina `MODELO_TEMPO`. No fim, cria a lista `FERRAMENTAS`.

**[01:15:38] Bloco 6** · _cartoes: Memória da sessão_  
A seção 6 detecta a GPU e carrega o Qwen. A seção 7 define as regras e o agente. A partir daqui, o notebook pode responder perguntas.

**[01:15:50] Bloco 7** · _fluxo: Uma pergunta atravessando o código_  
Agora a pergunta da célula 8.2: “Como vou da Biblioteca até a Mesa 3?”. A função `agente` monta as mensagens e chama `conversar`.

**[01:16:00] Bloco 8** · _fluxo: Uma pergunta atravessando o código_  
O Qwen responde com um pedido de ferramenta: `rota_tempo_previsto`, origem Biblioteca, destino Mesa 3. `ler_pedido_de_ferramenta` e `extrair_json` transformam o texto num dicionário.

**[01:16:12] Bloco 9** · _fluxo: Uma pergunta atravessando o código_  
`preparar_pedido` confere: Biblioteca e Mesa 3 existem e aparecem na pergunta, não há parâmetro extra, e o cenário vazio vira tranquilo. Status ok.

**[01:16:23] Bloco 10** · _fluxo: Uma pergunta atravessando o código_  
`executar` chama `rota_tempo_previsto`, que chama `prever_grafo_tempo`: o modelo da Fase 2 prevê o tempo dos 90 trechos no cenário tranquilo.

**[01:16:32] Bloco 11** · _fluxo: Uma pergunta atravessando o código_  
Com o grafo de segundos e a referência recalculada, a mesma `buscar` da Fase 1 roda o A estrela.

**[01:16:38] Bloco 12** · _grafo do campus (caminho Biblioteca → Eixo - Norte → Pátio/Direito → Pátio - D → Mesa 3; carrinho animado)_  
O caminho encontrado: Biblioteca, Eixo Norte, Pátio Direito, Pátio D, Mesa 3. São 113,5 metros e 43 segundos previstos.

**[01:16:50] Bloco 13** · _fluxo: Uma pergunta atravessando o código_  
O texto da ferramenta volta ao Qwen como mensagem tool. Ele escreve a explicação em português. Depois, `numeros_fora_da_ferramenta` compara os números: 113.5 e 43 estão no resultado. Nada sinalizado.

**[01:17:06] Bloco 14** · _fluxo: Uma pergunta atravessando o código_  
E a resposta final é impressa. Em resumo: o LLM entendeu e explicou, o modelo de custo deu os tempos, e a busca A estrela encontrou o caminho. As três fases numa só pergunta.

**[01:17:19] Bloco 15** · _topicos: Onde o tempo vai_  
Na GPU, essa pergunta inteira levou alguns segundos. O mapa e o treino rodam uma vez só; o Qwen é a parte cara de cada pedido.

## Capítulo 16 — Preparação para a defesa  (início 01:17:28, duração 00:08:03)

**[01:17:28] Bloco 1** · _titulo: Preparação para a defesa_  
Capítulo dezesseis: preparação para a defesa. Na arguição, cada um responde sobre a fase de outro colega, sozinho. Aqui estão perguntas prováveis, com respostas baseadas no código real.

**[01:17:42] Bloco 2** · _pergunta: Por que o projeto usa Python?_  
Pergunta 1. Por que o projeto usa Python?

**[01:17:46] Bloco 3** · _pergunta: Por que o projeto usa Python?_  
Porque é a linguagem da disciplina e do Colab, tem bibliotecas maduras para dados e modelos de linguagem, e permite um código curto e fácil de explicar.

**[01:17:56] Bloco 4** · _pergunta: Por que `VIZINHOS` é um dicionário?_  
Pergunta 2. Por que VIZINHOS é um dicionário?

**[01:18:00] Bloco 5** · _pergunta: Por que `VIZINHOS` é um dicionário?_  
Porque o algoritmo pergunta o tempo todo quais são os vizinhos de um local, e o dicionário responde direto pela chave. É uma lista de adjacência, ideal para um grafo esparso.

**[01:18:11] Bloco 6** · _pergunta: Por que a busca usa `while` e não `for`?_  
Pergunta 3. Por que a busca usa while e não for?

**[01:18:16] Bloco 7** · _pergunta: Por que a busca usa `while` e não `for`?_  
Porque o número de voltas não é conhecido antes. O laço roda enquanto houver itens na fronteira, e termina com return quando o destino é retirado.

**[01:18:25] Bloco 8** · _pergunta: Qual a diferença entre função e método?_  
Pergunta 4. Qual a diferença entre função e método?

**[01:18:30] Bloco 9** · _pergunta: Qual a diferença entre função e método?_  
Uma função existe sozinha, como min. Um método pertence a um objeto e é chamado com ponto, como fronteira ponto remove. O ponto acessa o que pertence ao objeto.

**[01:18:42] Bloco 10** · _pergunta: Como funciona `pergunta.strip().lower()`?_  
Pergunta 5. Como funciona pergunta.strip().lower()?

**[01:18:47] Bloco 11** · _pergunta: Como funciona `pergunta.strip().lower()`?_  
Strip devolve uma nova string sem os espaços das pontas, e lower age sobre esse resultado, deixando tudo minúsculo. É encadeamento, da esquerda para a direita, e a variável original não muda.

**[01:18:59] Bloco 12** · _pergunta: O que é a fronteira e por que ela é uma lista de tuplas?_  
Pergunta 6. O que é a fronteira e por que ela é uma lista de tuplas?

**[01:19:05] Bloco 13** · _pergunta: O que é a fronteira e por que ela é uma lista de tuplas?_  
É o conjunto de caminhos ainda não explorados. Cada item é uma tupla com f, g, local e caminho, e como o min compara tuplas posição por posição, a lista simples funciona como fila de prioridade.

**[01:19:18] Bloco 14** · _pergunta: Qual a diferença entre custo uniforme e A*?_  
Pergunta 7. Qual a diferença entre custo uniforme e A*?

**[01:19:23] Bloco 15** · _pergunta: Qual a diferença entre custo uniforme e A*?_  
O custo uniforme ordena pela distância já percorrida, g. O A estrela ordena por g mais h. No projeto, é a mesma função buscar, mudando só o parâmetro usar heurística.

**[01:19:35] Bloco 16** · _pergunta: Como vocês garantem que o caminho é ótimo?_  
Pergunta 8. Como vocês garantem que o caminho é ótimo?

**[01:19:40] Bloco 17** · _pergunta: Como vocês garantem que o caminho é ótimo?_  
Com três condições: a heurística é admissível e consistente, o objetivo é testado ao retirar o nó da fronteira, e todos os custos são positivos. Os custos do A estrela sempre bateram com os do custo uniforme.

**[01:19:54] Bloco 18** · _pergunta: Qual é a heurística e por que ela é admissível?_  
Pergunta 9. Qual é a heurística e por que ela é admissível?

**[01:19:59] Bloco 19** · _pergunta: Qual é a heurística e por que ela é admissível?_  
É o valor absoluto da diferença entre as distâncias do nó e do destino até a Entrada Principal. Pela desigualdade triangular, essa diferença nunca ultrapassa a distância real entre eles.

**[01:20:11] Bloco 20** · _pergunta: Por que não usaram distância euclidiana?_  
Pergunta 10. Por que não usaram distância euclidiana?

**[01:20:16] Bloco 21** · _pergunta: Por que não usaram distância euclidiana?_  
Porque o projeto não guarda coordenadas, só nomes e metros. A distância até um ponto de referência dá uma estimativa admissível usando apenas o próprio grafo.

**[01:20:26] Bloco 22** · _pergunta: O que acontece se a heurística retornar zero?_  
Pergunta 11. O que acontece se a heurística retornar zero?

**[01:20:31] Bloco 23** · _pergunta: O que acontece se a heurística retornar zero?_  
Então f é igual a g, e o A estrela vira o custo uniforme. Continua correto, mas perde a direção e pode expandir mais nós.

**[01:20:39] Bloco 24** · _pergunta: Por que, no experimento, o A* expandiu os mesmos nós?_  
Pergunta 12. Por que, no experimento, o A* expandiu os mesmos nós?

**[01:20:45] Bloco 25** · _pergunta: Por que, no experimento, o A* expandiu os mesmos nós?_  
Porque a origem do experimento é a própria Entrada, o ponto de referência. Aí quase todos os nós empatam em f. Com outra origem, como a Mesa 1, o A estrela expandiu 7 nós contra 9.

**[01:20:58] Bloco 26** · _pergunta: Qual a complexidade da busca do projeto?_  
Pergunta 13. Qual a complexidade da busca do projeto?

**[01:21:03] Bloco 27** · _pergunta: Qual a complexidade da busca do projeto?_  
A cada volta, min e remove percorrem a fronteira inteira. No pior caso, isso fica na ordem de E ao quadrado. Com heapq e um conjunto de visitados, cairia para E log E.

**[01:21:15] Bloco 28** · _pergunta: O que aconteceria se o campus fosse muito maior?_  
Pergunta 14. O que aconteceria se o campus fosse muito maior?

**[01:21:21] Bloco 29** · _pergunta: O que aconteceria se o campus fosse muito maior?_  
A lista com min ficaria lenta, e valeria trocar por heapq e usar um conjunto para os visitados. A tabela da heurística continuaria correta, mas o preparo custaria mais.

**[01:21:32] Bloco 30** · _pergunta: Como o modelo de custo foi treinado?_  
Pergunta 15. Como o modelo de custo foi treinado?

**[01:21:36] Bloco 31** · _pergunta: Como o modelo de custo foi treinado?_  
Com 2160 linhas sintéticas geradas por uma regra pública e semente fixa. Um Pipeline faz imputação, padronização e one hot, e a regressão linear venceu a árvore pela menor MAE na validação cruzada por trecho.

**[01:21:51] Bloco 32** · _pergunta: Por que separar treino e teste por trecho?_  
Pergunta 16. Por que separar treino e teste por trecho?

**[01:21:57] Bloco 33** · _pergunta: Por que separar treino e teste por trecho?_  
Porque o mesmo trecho no treino e no teste deixaria o teste fácil demais. Agrupando por trecho, medimos se o modelo prevê trechos que nunca viu.

**[01:22:07] Bloco 34** · _pergunta: O que significam MAE, RMSE e R²?_  
Pergunta 17. O que significam MAE, RMSE e R²?

**[01:22:13] Bloco 35** · _pergunta: O que significam MAE, RMSE e R²?_  
MAE é o erro absoluto médio, 0,84 segundo no teste. RMSE pune mais os erros grandes, 1,16 segundo. E R quadrado é a fração da variação que o modelo explica, 0,97.

**[01:22:30] Bloco 36** · _pergunta: Como o custo aprendido entra no A*?_  
Pergunta 18. Como o custo aprendido entra no A*?

**[01:22:34] Bloco 37** · _pergunta: Como o custo aprendido entra no A*?_  
Prever grafo tempo usa o modelo para trocar os metros por segundos previstos, a referência da heurística é recalculada em segundos, e a mesma função buscar da Fase 1 roda sobre esse grafo.

**[01:22:47] Bloco 38** · _pergunta: Mostre o modelo de custo mudando a decisão._  
Pergunta 19. Mostre o modelo de custo mudando a decisão.

**[01:22:52] Bloco 39** · _pergunta: Mostre o modelo de custo mudando a decisão._  
Da Mesa 1 até a Mesa 4 com cadeiras no pátio: a rota mais curta, por B, tem 42 metros e 35,7 segundos. O A estrela com tempo escolhe a rota por D, com 46 metros e 23,7 segundos.

**[01:23:08] Bloco 40** · _pergunta: Como o LLM decide qual ferramenta chamar?_  
Pergunta 20. Como o LLM decide qual ferramenta chamar?

**[01:23:13] Bloco 41** · _pergunta: Como o LLM decide qual ferramenta chamar?_  
Ele lê as regras, a pergunta e a ficha em JSON de cada ferramenta, gerada pela docstring. Então escreve um pedido entre as marcas tool call. Quem executa é o código.

**[01:23:24] Bloco 42** · _pergunta: Por que o LLM não calcula a rota?_  
Pergunta 21. Por que o LLM não calcula a rota?

**[01:23:29] Bloco 43** · _pergunta: Por que o LLM não calcula a rota?_  
Porque modelos de linguagem não são confiáveis em cálculos exatos de caminhos. A busca é exata e verificável. O modelo entende o pedido e explica; a ferramenta calcula.

**[01:23:42] Bloco 44** · _pergunta: Quando o LLM alucina, e o que o código faz?_  
Pergunta 22. Quando o LLM alucina, e o que o código faz?

**[01:23:48] Bloco 45** · _pergunta: Quando o LLM alucina, e o que o código faz?_  
Na versão 4, ele inventou rotas sem chamar ferramenta; hoje o código pede de novo e, se não conseguir, admite. Locais inventados são recusados, e números fora do resultado são sinalizados.

**[01:24:01] Bloco 46** · _pergunta: Quanto custa e quanto demora cada chamada?_  
Pergunta 23. Quanto custa e quanto demora cada chamada?

**[01:24:06] Bloco 47** · _pergunta: Quanto custa e quanto demora cada chamada?_  
Não há custo por chamada, porque o modelo roda na sessão, sem chave de API. Mas há tempo: mediana de 3,8 segundos por pedido na GPU e 135 segundos na CPU do Colab.

**[01:24:19] Bloco 48** · _pergunta: E se o usuário pedir algo fora do escopo?_  
Pergunta 24. E se o usuário pedir algo fora do escopo?

**[01:24:24] Bloco 49** · _pergunta: E se o usuário pedir algo fora do escopo?_  
Se for uma saudação ou pergunta geral, ele responde sem ferramenta, como na capital do Brasil. Se for um local que não existe, como B-07, o programa pede um nome do mapa.

**[01:24:36] Bloco 50** · _pergunta: Por que existe `preparar_pedido` se o LLM já escolhe os argumentos?_  
Pergunta 25. Por que existe preparar_pedido se o LLM já escolhe os argumentos?

**[01:24:43] Bloco 51** · _pergunta: Por que existe `preparar_pedido` se o LLM já escolhe os argumentos?_  
Porque um modelo pequeno erra. Preparar pedido padroniza os nomes e confere tudo antes de executar, devolvendo ok, erro ou esclarecimento. O modelo interpreta, e o código garante.

**[01:24:55] Bloco 52** · _pergunta: Quais são as limitações do projeto?_  
Pergunta 26. Quais são as limitações do projeto?

**[01:25:00] Bloco 53** · _pergunta: Quais são as limitações do projeto?_  
Os dados são sintéticos, as distâncias são estimativas e não há sensores. O Qwen pequeno acerta só 3 de 10 pedidos informais. E o agente calcula um destino por vez, com experimento em recortes do mesmo mapa.

**[01:25:15] Bloco 54** · _titulo: Boa apresentação!_  
Uma dica final: na arguição, explique com as palavras do código. Cite a função, a linha e o número real. Você passou por todo o projeto: o grafo, a busca, a heurística, o A estrela, o modelo de custo e o agente. Boa apresentação!
