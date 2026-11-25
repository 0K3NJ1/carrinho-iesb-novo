from base import *
from dados import T, br, estados_do_passo

UCS = T['ucs_mesa1_mesa4']


def cena_ucs(i, final=False):
    p = UCS['passos'][i]
    linhas = [[f['local'], br(f['g'], 1 if isinstance(f['g'], float) and not float(f['g']).is_integer() else 0)] for f in p['fronteira']]
    estilos = ['dest' if j == 0 else '' for j in range(len(linhas))]
    est = estados_do_passo(UCS, i)
    caminho = p['escolhido']['caminho'] if final else []
    if final:
        est.update({n: 'caminho' for n in caminho})
    vis = ', '.join(p['visitados']) or '(vazio)'
    return dividido(
        grafo(camera=PATIO_LADO, rotulos='todos', pesos=True, unidadePeso=' m', zoomTexto=1.25, estados=est, caminho=caminho,
              legendaCores=[('atual', 'escolhido'), ('fronteira', 'fronteira'), ('expandido', 'visitado')]),
        tabela('Fronteira (custo uniforme)', ['local', 'g (metros)'], linhas, estilos=estilos, fonte=25,
               rodape=f'**início da volta {i + 1}**<br>**visitados:** {vis}'), .55)


FALAS = [
    'Volta 1. A fronteira tem só a origem, Mesa 1, com custo zero. Ela é escolhida, não é o destino e ainda não foi visitada. Então é expandida: seu único vizinho, Pátio A, entra com g igual a 2.',
    'Volta 2. O único item é Pátio A, com g 2. Ao expandir, entram Pátio B, com 2 mais 20, igual a 22, e Pátio D, com 2 mais 18, igual a 20. Mesa 1 já foi visitada e não volta.',
    'Volta 3. O menor custo é Pátio D, com 20. Ele entra em visitados, e seus vizinhos entram: Pátio Direito com 44 e Mesa 3 com 22.',
    'Volta 4. Agora há um empate em 22: Mesa 3 e Pátio B. O `min` compara tuplas posição por posição: f igual, g igual, então desempata pelo nome. “Mesa 3” vem antes de “Pátio B” na ordem alfabética.',
    'Mesa 3 é expandida, mas não tem vizinhos novos. Volta 5: Pátio B, com 22, é expandido. Entram Pátio Direito com 40, Mesa 2 e Easy Smart com 24, e Café Mania com 26.',
    'Repare que Pátio Direito aparece duas vezes na fronteira: com 44, vindo por D, e com 40, vindo por B. O código não apaga a cópia pior; ela fica lá e será ignorada se for escolhida depois.',
    'Voltas 6, 7 e 8: Easy Smart, Mesa 2 e Café Mania, todos perto de 24 e 26, são expandidos e não acrescentam nada. A busca gasta tempo com eles porque não sabe onde fica o destino.',
    'Volta 9. O menor agora é Pátio Direito com 40. Ao expandi-lo, Mesa 4 entra com 40 mais 2, igual a 42, junto com o Eixo Norte, a Sala dos Professores e os banheiros.',
    'Volta 10. O menor custo é Mesa 4, com 42. Agora sim, ao ser retirada da fronteira, ela é o destino. A função devolve o caminho, o custo 42 e 9 nós expandidos.',
]

blocos = [
    bloco('Capítulo cinco. Já temos o grafo. Agora, como um programa encontra o melhor caminho dentro dele? Esta é a pergunta da busca em Inteligência Artificial.',
          titulo('A busca e o custo uniforme', 'A função `buscar`, a fronteira e cada volta do laço com dados reais', 'Capítulo 5')),
    bloco('Buscar é explorar estados a partir da origem até achar o objetivo. Uma busca não informada só conhece o custo já percorrido. Uma busca informada usa também uma estimativa do que falta.',
          topicos('Busca em IA', ['**Não informada**: só sabe o custo já pago (ex.: custo uniforme)',
                                  '**Informada**: usa também uma estimativa até o objetivo (ex.: A*)',
                                  'As duas, no projeto, são **a mesma função** `buscar`',
                                  'A diferença é o parâmetro `usar_heuristica`'], mostrar=4)),
    bloco('A busca de custo uniforme sempre expande o nó de menor custo acumulado desde a origem. Esse custo se chama g. Com custos positivos, o primeiro caminho que chega ao destino é o mais barato.',
          formula([('prioridade', 'proc'), ('='), ('g(n)', 'destaque')],
                   ['`g(n)`: soma dos pesos da origem até o nó `n`', 'expande sempre o menor `g` da fronteira'], 'Custo uniforme')),
    bloco('Agora a função `buscar`, linha por linha. Ela recebe a origem, o destino, o grafo, um booleano dizendo se usa a heurística, e a tabela de referência da heurística.',
          codigo(7, 13, janela=(13, 33))),
    bloco('Se a referência não for passada, usa a tabela `DISTANCIA_ENTRADA`. E se a origem ou o destino não existirem no grafo, a função devolve `None`, `None` e zero, sem procurar.',
          codigo(7, (14, 17), janela=(13, 33))),
    bloco('A linha 18 calcula a estimativa da origem. No custo uniforme, `usar_heuristica` é falso, então a estimativa é zero.',
          codigo(7, 18, janela=(13, 33))),
    bloco('A fronteira é a lista dos caminhos que ainda podem ser explorados. Cada item é uma tupla com quatro valores: f, g, o local e o caminho até ele.',
          codigo(7, 19, janela=(13, 33), notas=[(19, '(f, g, local, caminho)')])),
    bloco('`visitados` guarda os locais já expandidos, e `expandidos` conta quantos foram. Essa contagem é a métrica do experimento.',
          codigo(7, (20, 21), janela=(13, 33))),
    bloco('O laço `while` roda enquanto a fronteira não estiver vazia. A cada volta, ele escolhe um item, testa e, se for o caso, expande.',
          codigo(7, 22, janela=(13, 38))),
    bloco('Se a fronteira esvaziar sem achar o destino, não existe caminho entre os dois locais, e a linha 38, já fora do laço, devolve `None`, `None` e a contagem de expandidos.',
          codigo(7, 38, janela=(13, 38), notas=[(38, 'sem caminho')])),
    bloco('`min(fronteira)` escolhe a menor tupla. Python compara tuplas posição por posição: primeiro o f, depois o g, depois o nome do local. Por isso a primeira posição da tupla é a prioridade.',
          codigo(7, 23, janela=(13, 38), notas=[(23, 'compara f, depois g, depois o nome')])),
    bloco('Esta é a fila de prioridade do projeto: uma lista comum com `min`. Em projetos grandes se usa `heapq`, que é mais rápido; aqui, com 90 nós, a lista simples é suficiente e mais fácil de explicar.',
          codigo(7, (23, 24), janela=(13, 38), notas=[(24, 'retira o escolhido da fronteira')])),
    bloco('A linha 25 desempacota a tupla escolhida em quatro nomes. Se o local é o destino, a busca termina e devolve o caminho, o custo g e os expandidos.',
          codigo(7, (25, 27), janela=(13, 38))),
    bloco('Detalhe importante: o teste de objetivo acontece quando o nó sai da fronteira, e não quando entra. É isso que garante o caminho mais barato.',
          codigo(7, 26, janela=(13, 38), notas=[(26, 'objetivo testado ao RETIRAR')])),
    bloco('Se o local já foi visitado, `continue` pula para a próxima volta. Isso descarta cópias antigas e piores do mesmo local que ficaram na fronteira.',
          codigo(7, (28, 29), janela=(13, 38))),
    bloco('Senão, o local entra em `visitados` e o contador aumenta. Depois, o `for` percorre os vizinhos. Para cada vizinho ainda não visitado, calcula o novo g: o g atual mais o custo da ligação.',
          codigo(7, (30, 34), janela=(13, 38))),
    bloco('E acrescenta na fronteira uma tupla nova, com o caminho estendido. Repare que `caminho + [vizinho]` cria uma lista nova: o caminho de cada item da fronteira é independente.',
          codigo(7, (35, 37), janela=(13, 38), notas=[(37, 'nova lista, não altera a antiga')])),
    bloco('Vamos ver tudo isso funcionando com dados reais: custo uniforme da Mesa 1 até a Mesa 4. Estas são exatamente as voltas que a função executa.',
          cena_ucs(0)),
]
for i, fala in enumerate(FALAS[:5]):
    blocos.append(bloco(fala, cena_ucs(min(i, 4)) if i < 4 else cena_ucs(4)))
blocos.append(bloco(FALAS[5], cena_ucs(5)))
blocos.append(bloco(FALAS[6], cena_ucs(7)))
blocos.append(bloco(FALAS[7], cena_ucs(8)))
blocos.append(bloco(FALAS[8], cena_ucs(9, final=True)))
blocos += [
    bloco('O carrinho segue o caminho encontrado: Mesa 1, Pátio A, Pátio B, Pátio Direito e Mesa 4, com 42 metros no total.',
          grafo(camera=PATIO_LARGO, rotulos='todos', pesos=True, unidadePeso=' m', zoomTexto=1.15, caminho=UCS['caminho'],
                estados={n: 'caminho' for n in UCS['caminho']}, carrinho=dict(caminho=UCS['caminho'])), 3.5),
    bloco('Vantagens do custo uniforme: é completo, porque acha um caminho se ele existir, e é ótimo com custos positivos. A limitação: expande em todas as direções, inclusive para longe do destino.',
          topicos('Custo uniforme: balanço', ['**Completo**: encontra caminho se existir',
                                              '**Ótimo** com custos positivos (testa o objetivo ao retirar)',
                                              '**Limitação**: expande para todos os lados, sem direção',
                                              'Aqui: 9 nós expandidos para um caminho de 4 passos'], mostrar=4)),
    bloco('Neste exemplo, ele expandiu 9 nós, incluindo Mesa 3, Easy Smart, Mesa 2 e Café Mania, que não ajudam a chegar à Mesa 4. No próximo capítulo, vamos dar uma direção à busca: a heurística.',
          titulo('Próximo: a heurística', 'Uma estimativa que aponta para o destino', 'Capítulo 5 concluído')),
]

CAPITULO = dict(numero=5, titulo='A busca de custo uniforme', blocos=blocos)
