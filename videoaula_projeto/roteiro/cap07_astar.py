from base import *
from dados import T, br, estados_do_passo

AS = T['astar_mesa1_mesa4']
UCS = T['ucs_mesa1_mesa4']


def n(x):
    x = float(x)
    return br(x, 0) if x.is_integer() else br(x, 1)


def cena_as(i, final=False):
    p = AS['passos'][i]
    linhas = [[f['local'], n(f['g']), n(f['h']), n(f['f'])] for f in p['fronteira']]
    estilos = ['dest' if j == 0 else '' for j in range(len(linhas))]
    est = estados_do_passo(AS, i)
    caminho = p['escolhido']['caminho'] if final else []
    if final:
        est.update({x: 'caminho' for x in caminho})
    vis = ', '.join(p['visitados']) or '(vazio)'
    return dividido(
        grafo(camera=PATIO_LADO, rotulos='todos', pesos=True, unidadePeso=' m', zoomTexto=1.25, estados=est, caminho=caminho,
              legendaCores=[('atual', 'escolhido'), ('fronteira', 'fronteira'), ('expandido', 'visitado')]),
        tabela('Fronteira do A* (ordenada por f)', ['local', 'g', 'h', 'f'], linhas, estilos=estilos, fonte=24,
               rodape=f'**início da volta {i + 1}**<br>**visitados:** {vis}'), .52)


blocos = [
    bloco('Capítulo sete: o A estrela, o algoritmo central da Fase 1. Ele junta as duas ideias que já vimos: o custo já percorrido e a estimativa do que falta.',
          titulo('O algoritmo A*', 'f(n) = g(n) + h(n), com as voltas reais de Mesa 1 até Mesa 4', 'Capítulo 7')),
    bloco('A prioridade de cada nó na fronteira é f de n, a soma de g de n e h de n.',
          formula([('f(n)', 'proc'), ('='), ('g(n)', 'destaque'), ('+'), ('h(n)', 'alerta')], [], 'A fórmula do A*')),
    bloco('g de n é o custo real já pago, da origem até n. É a soma dos metros das ligações percorridas.',
          formula([('f(n)', 'proc'), ('='), ('g(n)', 'destaque'), ('+'), ('h(n)', 'alerta')],
                   ['`g(n)`: custo **real** da origem até `n`'], 'A fórmula do A*', realce=[2])),
    bloco('h de n é a estimativa do que ainda falta, de n até o destino, dada pela heurística do capítulo anterior.',
          formula([('f(n)', 'proc'), ('='), ('g(n)', 'destaque'), ('+'), ('h(n)', 'alerta')],
                   ['`g(n)`: custo **real** da origem até `n`', '`h(n)`: **estimativa** de `n` até o destino'], 'A fórmula do A*', realce=[4])),
    bloco('E f de n estima o custo total de um caminho que passa por n. Somar faz sentido porque as duas partes estão na mesma unidade, metros, e juntas cobrem o trajeto inteiro: o que já foi e o que falta.',
          formula([('f(n)', 'proc'), ('='), ('g(n)', 'destaque'), ('+'), ('h(n)', 'alerta')],
                   ['`g(n)`: custo **real** da origem até `n`', '`h(n)`: **estimativa** de `n` até o destino',
                    '`f(n)`: estimativa do **custo total** passando por `n`'], 'A fórmula do A*')),
    bloco('No código, o A estrela é a mesma função `buscar`, com `usar_heuristica` verdadeiro. A linha 35 calcula h do vizinho, e a linha 36 guarda na fronteira o novo g mais a estimativa, que é o f.',
          codigo(7, (34, 37), janela=(13, 38), notas=[(36, 'primeira posição: f = g + h')])),
    bloco('Como f é a primeira posição da tupla, o `min` da linha 23 escolhe automaticamente o menor f. Em empate de f, escolhe o menor g; em empate de g, a ordem alfabética do nome.',
          codigo(7, 23, janela=(13, 38), notas=[(23, 'menor f, depois g, depois nome')])),
    bloco('A função `a_estrela` é só um atalho: chama `buscar` com o grafo de metros e a heurística ligada, e devolve o caminho e o custo.',
          codigo(7, (41, 43), janela=(28, 48))),
    bloco('Agora, a mesma consulta do capítulo cinco, Mesa 1 até Mesa 4, com o A estrela. No início da volta 1, a fronteira tem só a origem: g zero, h 38, pois 127,5 menos 89,5 dá 38. Então f é 38.',
          cena_as(0)),
    bloco('Início da volta 2. Ao expandir a Mesa 1, entrou Pátio A, com g 2 e h 36, pois 125,5 menos 89,5 dá 36. f é 38, e ele é o único da fronteira.',
          cena_as(1)),
    bloco('Início da volta 3. Ao expandir Pátio A, entraram Pátio B, com g 22 e h 16, f 38, e Pátio D, com g 20 e h 22, f 42. Repare: D tem g menor, mas B parece mais perto do destino.',
          cena_as(2)),
    bloco('Por isso o A estrela escolhe Pátio B, com f 38. O custo uniforme tinha escolhido Pátio D, só porque o g era menor. A heurística mudou a ordem.',
          cena_as(2)),
    bloco('Início da volta 4. Pátio B foi expandido e entraram Pátio Direito, Mesa 2 e Easy Smart, todos com f 42, e Café Mania, com f 46.',
          cena_as(3)),
    bloco('Agora há vários empates em 42. Pela regra da tupla, ganha o menor g: Pátio D, com g 20. Ao ser expandido, ele acrescenta Mesa 3 e uma segunda cópia de Pátio Direito, as duas com f 46.',
          cena_as(3)),
    bloco('Voltas 5 e 6: Easy Smart e Mesa 2, com f 42 e g 24, são expandidos sem novidade. Os empates fazem o A estrela gastar duas expansões que não ajudam.',
          cena_as(5)),
    bloco('Início da volta 7. Pátio Direito, com g 40 e h 2, f 42, é escolhido e expandido. Mesa 4 entra com g 42 e h zero: f 42.',
          cena_as(6)),
    bloco('Volta 8. Mesa 4 é retirada com f 42 e é o destino. Caminho: Mesa 1, Pátio A, Pátio B, Pátio Direito, Mesa 4. Custo 42 metros, o mesmo do custo uniforme.',
          cena_as(7, final=True)),
    bloco('A diferença está no trabalho: o A estrela expandiu 7 nós, contra 9 do custo uniforme. Mesa 3 e Café Mania ficaram na fronteira com f 46 e nunca precisaram ser expandidos.',
          tabela('Mesma consulta, Mesa 1 → Mesa 4 (valores reais)', ['algoritmo', 'custo', 'nós expandidos', 'voltas do laço'],
                 [['Custo uniforme', '42 m', str(UCS['expandidos']), str(len(UCS['passos']))],
                  ['A*', '42 m', str(AS['expandidos']), str(len(AS['passos']))]], estilos=['', 'ok'], fonte=30)),
    bloco('Veja o carrinho percorrendo o caminho escolhido.',
          grafo(camera=PATIO_LARGO, rotulos='todos', pesos=True, unidadePeso=' m', zoomTexto=1.15, caminho=AS['caminho'],
                estados={x: 'caminho' for x in AS['caminho']}, carrinho=dict(caminho=AS['caminho'])), 3.5),
    bloco('Quando o A estrela garante o caminho ótimo? Quando a heurística é admissível e o objetivo é testado ao retirar o nó da fronteira, como na linha 26.',
          topicos('Quando o A* é ótimo', ['Heurística **admissível**: nunca superestima',
                                          'Objetivo testado ao **retirar** da fronteira (linha 26)',
                                          'Com heurística **consistente**, o primeiro `g` de cada nó retirado já é o menor',
                                          'O projeto tem as três condições'], mostrar=4)),
    bloco('Por que o primeiro caminho encontrado pode não ser ótimo em outras implementações? Se o teste de objetivo fosse feito ao inserir o vizinho, um caminho caro poderia ser devolvido antes de outro mais barato aparecer.',
          codigo(7, (26, 27), janela=(13, 38), notas=[(26, 'se testasse ao inserir, poderia errar')])),
    bloco('E se a heurística for zero? Então f é igual a g, e o A estrela vira exatamente o custo uniforme. É isso que o projeto faz quando `usar_heuristica` é falso.',
          formula([('h(n) = 0', 'alerta'), ('⇒'), ('f(n) = g(n)', 'destaque')], ['A* sem heurística = custo uniforme'])),
    bloco('E a busca gulosa? Ela usa só h de n, ignorando o custo já pago. É rápida, mas não garante o melhor caminho. O A estrela equilibra as duas coisas.',
          tabela('Três buscas, uma diferença: a prioridade', ['algoritmo', 'prioridade', 'ótimo?'],
                 [['Custo uniforme', '`g(n)`', 'sim'], ['Gulosa', '`h(n)`', 'não'], ['A*', '`g(n) + h(n)`', 'sim, com h admissível']],
                 estilos=['', 'erro', 'ok'], fonte=30)),
    bloco('Agora, um caso em que a heurística do projeto não ajuda nada: quando a origem é a própria Entrada Principal. Da entrada até a Mesa 4, os dois algoritmos expandem os mesmos 4 nós.',
          tabela('Entrada Principal → Mesa 4 (valores reais)', ['algoritmo', 'custo', 'nós expandidos'],
                 [['Custo uniforme', '89,5 m', str(T['ucs_entrada_mesa4']['expandidos'])],
                  ['A*', '89,5 m', str(T['astar_entrada_mesa4']['expandidos'])]], fonte=30)),
    bloco('O motivo é matemático. Para um nó n que a busca alcança vindo da entrada, g de n é igual à distância da entrada até n. Então f igual a g mais o destino menos g dá sempre o mesmo valor.',
          formula([('f(n)', 'proc'), ('='), ('d(E,n)', 'destaque'), ('+'), ('(d(E,dest) − d(E,n))', 'alerta'), ('='), ('d(E,dest)', 'caminho')],
                   ['com origem = Entrada, quase todos os nós empatam em `f`', 'o desempate por `g` reproduz a ordem do custo uniforme'])),
    bloco('Isso explica o experimento da Fase 1, que mede tudo a partir da entrada. Guarde esse ponto para a defesa: não é erro de implementação, é a escolha do ponto de referência.',
          topicos('Para a defesa', ['A* e custo uniforme dão **o mesmo custo** (corretos)',
                                    'Da Entrada, expandem o mesmo número de nós: empate de `f`',
                                    'De Mesa 1 até Mesa 4: **7 contra 9** expansões',
                                    'Complexidade: a lista com `min` custa O(tamanho da fronteira) por volta'], mostrar=4)),
    bloco('Sobre complexidade: cada ligação pode colocar um item na fronteira, e a cada volta `min` e `remove` percorrem a fronteira inteira. No pior caso, isso dá algo da ordem de E ao quadrado, onde E é o número de ligações.',
          topicos('Complexidade', ['Cada volta: `min(fronteira)` e `remove` percorrem a lista inteira',
                                   'A fronteira pode ter até ~2E itens; o laço roda até ~2E vezes',
                                   'Pior caso do projeto: O(E²), mais as buscas em `visitados` (lista)',
                                   'Com `heapq` e um `set` de visitados: O(E log E)'], mostrar=4, fonte=32)),
    bloco('Com `heapq` e um conjunto para os visitados, cairia para E vezes log de E. Mas com 90 ligações, a versão simples resolve cada busca em centésimos de milissegundo, e é bem mais fácil de explicar.',
          topicos('Complexidade', ['Cada volta: `min(fronteira)` e `remove` percorrem a lista inteira',
                                   'A fronteira pode ter até ~2E itens; o laço roda até ~2E vezes',
                                   'Pior caso do projeto: O(E²), mais as buscas em `visitados` (lista)',
                                   'Com `heapq` e um `set` de visitados: O(E log E)'], mostrar=4, fonte=32)),
]

CAPITULO = dict(numero=7, titulo='O algoritmo A*', blocos=blocos)
